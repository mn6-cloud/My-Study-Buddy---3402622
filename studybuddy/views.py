# studybuddy/views.py
import re
from django.shortcuts import render
from .models import Section, Quiz, Question, QAPair
from django.shortcuts import get_object_or_404

def topic_summary(request):
    topic = request.GET.get('topic', '')
    sections = Section.objects.filter(topic__icontains=topic)
    summary = ' '.join([s.content.split('. ')[0] + '.' for s in sections[:3]]) if sections else "No summary found."
    return render(request, 'topic_summary.html', {'summary': summary})

def quiz_list(request):
    quizzes = Quiz.objects.all()
    return render(request, 'quiz_list.html', {'quizzes': quizzes})

# def take_quiz(request, topic):
#     try:
#         quiz = Quiz.objects.get(topic=topic)
#     except Quiz.DoesNotExist:
#         return render(request, 'quiz_error.html', {'topic': topic})
    
#     questions = Question.objects.filter(quiz=quiz).order_by('?')[:5]
    
#     quiz = get_object_or_404(Quiz, topic=topic)
#     questions = Question.objects.filter(quiz=quiz).order_by('?')[:5]  # Random 5 questions
    
#     if request.method == 'POST':
#         # Grade answers (simplified)
#         score = 0
#         feedback = []
#         for q in questions:
#             user_answer = request.POST.get(f'q{q.id}', '')
#             if user_answer == q.correct_answer:
#                 score += 1
#             feedback.append({
#                 'question': q.text,
#                 'correct': q.correct_answer,
#                 'explanation': q.explanation
#             })
#         return render(request, 'quiz_result.html', {'score': score, 'feedback': feedback})
    
#     return render(request, 'quiz.html', {'questions': questions})

# studybuddy/views.py
def take_quiz(request, quiz_slug):  # Changed from "topic" to "quiz_slug"
    quiz = get_object_or_404(Quiz, slug=quiz_slug)
    questions = Question.objects.filter(quiz=quiz).order_by('?')[:5]

    if request.method == 'POST':
        score = 0
        feedback = []
        for q in questions:
            user_answer = request.POST.get(f'q{q.id}', '')
            if user_answer == q.correct_answer:
                score += 1
            feedback.append({
                'question': q.text,
                'correct': q.correct_answer,
                'explanation': q.explanation
            })
        return render(request, 'quiz_result.html', {'score': score, 'feedback': feedback})
    
    return render(request, 'quiz.html', {'quiz': quiz, 'questions': questions})

def chatbot(request):
    answer = ""
    if request.method == 'POST':
        query = request.POST.get('query', '').lower()
        query = re.sub(r'[^\w\s]', '', query)  # Remove punctuation
        keywords = query.split()
        
        # Check for matches
        for keyword in keywords:
            match = QAPair.objects.filter(keyword=keyword).first()
            if match:
                answer = match.answer
                break
        if not answer:
            answer = "Sorry, I don't know that. Ask something else!"
    
    return render(request, 'chatbot.html', {'answer': answer})