# studybuddy/admin.py
from django.contrib import admin
from .models import Document, Section, Quiz, Question, QAPair

class QuizAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}

admin.site.register(Document)
admin.site.register(Section)
admin.site.register(Quiz, QuizAdmin)
admin.site.register(Question)
admin.site.register(QAPair)