from django.db import models
from django.contrib.contenttypes.models import ContentType
from lessons.models import Language, Problem
from userstatus.models import UserProblemStatus
from savollar.models import Question, Quiz
from users.models import MyUser
# from lessons.models import Problem, Language



class Solution(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    language = models.ForeignKey(Language, on_delete=models.CASCADE)  
    code = models.TextField()
    is_accepted = models.BooleanField(default=False)
    execution_time = models.FloatField(default=0.0)  
    memory_usage = models.FloatField(default=0.0)  
    score = models.PositiveIntegerField(default=0)  
    passed_tests = models.PositiveIntegerField(default=0)  
    total_tests = models.PositiveIntegerField(default=0)  
    created_at = models.DateTimeField(auto_now_add=True)  
    updated_at = models.DateTimeField(auto_now=True)  

    # class Meta:
    #     unique_together = ('user', 'problem', 'language')  

    def __str__(self):
        return f"{self.user.email} - {self.problem.title} ({self.language}) - {'Accepted' if self.is_accepted else 'Pending'}"

    @classmethod
    def create(cls, user, problem, language, code, execution_time, memory_usage, passed_tests, total_tests):
        solution = cls.objects.create(
            user=user,
            problem=problem,
            language=language,
            code=code,
            execution_time=execution_time,
            memory_usage=memory_usage,
            passed_tests=passed_tests,
            total_tests=total_tests,
            is_accepted=passed_tests == total_tests  
        )
        solution.save()

        # Agar bu yechim qabul qilinsa, foydalanuvchi bu muammoni hal qilgan deb saqlash
        if solution.is_accepted:
            UserProblemStatus.mark_completed(user, problem)

        return solution




class UserQuizResult(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    score = models.PositiveIntegerField(default=0)  # To'plangan ball
    correct_answers = models.PositiveIntegerField(default=0)  # To'g'ri javoblar soni
    total_questions = models.PositiveIntegerField(default=0)  # Jami savollar
    completed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'quiz')  # Har bir foydalanuvchi har bir quiz uchun faqat bitta natijaga ega bo'lishi kerak

    def __str__(self):
        return f"{self.user.email} - {self.quiz.title} - {self.score} points"

    @classmethod
    def log_quiz_result(cls, user, quiz, correct_answers, total_questions):
        """Foydalanuvchining quiz natijalarini saqlash"""
        score = correct_answers * 10  # Har bir to‘g‘ri javob uchun 10 ball
        result, created = cls.objects.get_or_create(user=user, quiz=quiz)
        result.correct_answers = correct_answers
        result.total_questions = total_questions
        result.score = score
        result.save()
        return result

class UserQuestionResult(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    is_correct = models.BooleanField(default=False)  # Foydalanuvchi javobi to‘g‘rimi?
    answered_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'question')  # Har bir foydalanuvchi har bir savolga faqat bitta natija ega bo‘lishi mumkin

    def __str__(self):
        return f"{self.user.email} - {self.question.id} - {'✅' if self.is_correct else '❌'}"

    @classmethod
    def create_answer(cls, user, question, is_correct):
        result, created = cls.objects.get_or_create(user=user, question=question)
        result.is_correct = is_correct
        result.save()
        return result


class AnswerTrue(UserQuestionResult):
    class Meta:
        proxy=True

    def is_true(self):
        if self.is_correct:
            self.is_correct=True
            self.save()
        
        