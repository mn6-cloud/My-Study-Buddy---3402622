# studybuddy/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Document, Section
import PyPDF2
from docx import Document as DocxDocument
import os

@receiver(post_save, sender=Document)
def process_document(sender, instance, created, **kwargs):
    if created:
        file_path = instance.file.path
        sections = []
        
        # Extract text based on file type
        if file_path.endswith('.pdf'):
            with open(file_path, 'rb') as f:
                reader = PyPDF2.PdfReader(f)
                text = ''.join([page.extract_text() for page in reader.pages])
        elif file_path.endswith('.docx'):
            doc = DocxDocument(file_path)
            text = '\n'.join([para.text for para in doc.paragraphs])
        else:  # Assume .txt
            with open(file_path, 'r') as f:
                text = f.read()
        
        # Split text into sections (simplified: split by "TOPIC: ")
        raw_sections = text.split('TOPIC: ')[1:]  # Skip text before first TOPIC
        for sec in raw_sections:
            topic_end = sec.find('\n')
            topic = sec[:topic_end].strip()
            content = sec[topic_end:].strip()
            sections.append(Section(document=instance, topic=topic, content=content))
        
        # Bulk create sections
        Section.objects.bulk_create(sections)