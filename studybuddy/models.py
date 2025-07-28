# studybuddy/models.py
from django.db import models
from django.utils.text import slugify

class Document(models.Model):
    title = models.CharField(max_length=200)
    file = models.FileField(upload_to='documents/')
    upload_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title

class Section(models.Model):
    document = models.ForeignKey(Document, on_delete=models.CASCADE)
    topic = models.CharField(max_length=100)
    content = models.TextField()

    def __str__(self):
        return self.topic
    
class Quiz(models.Model):
    title = models.CharField(max_length=100)
    topic = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True, null=True)  # New field for slug)  # New field

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.title and self.topic

class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    text = models.TextField()
    option_a = models.CharField(max_length=200)
    option_b = models.CharField(max_length=200)
    option_c = models.CharField(max_length=200)
    correct_answer = models.CharField(max_length=1)  # 'A', 'B', or 'C'
    explanation = models.TextField()
    
    def __str__(self):
        return self.text

class QAPair(models.Model):
    keyword = models.CharField(max_length=50, unique=True)
    answer = models.TextField()
    
    def __str__(self):
        return self.keyword