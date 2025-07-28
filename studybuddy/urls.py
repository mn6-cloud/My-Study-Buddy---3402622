# studybuddy/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('summary/', views.topic_summary, name='topic_summary'),
    path('quizzes/', views.quiz_list, name='quiz_list'),
    # path('quiz/<str:topic>/', views.take_quiz, name='take_quiz'),
    path('quiz/<slug:quiz_slug>/', views.take_quiz, name='take_quiz'),
    path('chatbot/', views.chatbot, name='chatbot'),
]