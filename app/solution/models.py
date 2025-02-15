from django.db import models
from django.contrib.contenttypes.models import ContentType
from savollar.models import Question, Quiz
from users.models import MyUser
from lessons.models import Problem, Language




# Foydalanuvchining yechimi
class Solution(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    language = models.ForeignKey(Language, on_delete=models.CASCADE)  # 🔥 Dasturlash tili
    code = models.TextField()
    is_accepted = models.BooleanField(default=False)
    execution_time = models.FloatField(default=0.0)  # Bajarilish vaqti (soniyalarda)
    memory_usage = models.FloatField(default=0.0)  # RAM ishlatilishi (MB)
    score = models.PositiveIntegerField(default=0)  # Baholash tizimi
    passed_tests = models.PositiveIntegerField(default=0)  # Nechta testdan o'tgan
    total_tests = models.PositiveIntegerField(default=0)  # Jami testlar soni
    created_at = models.DateTimeField(auto_now_add=True)  # Yaratilgan vaqt
    updated_at = models.DateTimeField(auto_now=True)  # Yangilangan vaqt

    # class Meta:
    #     unique_together = ('user', 'problem', 'language')  # Har bir user har bir problemni har xil tilda yechishi mumkin

    def __str__(self):
        return f"{self.user.email} - {self.problem.title} ({self.language}) - {'Accepted' if self.is_accepted else 'Pending'}"

    def calculate_score(self):
        """Baholash: testlar, vaqt va RAM asosida hisoblash"""
        if self.total_tests == 0:
            return 0

        accuracy = self.passed_tests / self.total_tests
        base_score = 100  # Maksimal ball

        # 🕒 Vaqt jazosini hisoblash
        time_penalty = min(self.execution_time * 2, 30)  # Har sekundga 2 ball chegirma, maksimal -30 ball

        # 🖥️ RAM jazosini hisoblash
        ram_penalty = min(self.memory_usage * 0.5, 20)  # Har 1 MB RAM uchun 0.5 ball chegirma, maksimal -20 ball

        # Yakuniy baho hisoblash
        self.score = max(int(base_score * accuracy - time_penalty - ram_penalty), 0)  # Minimal baho 0 bo‘lishi kerak

    @classmethod
    def log_solution(cls, user, problem, language, code, execution_time, memory_usage, passed_tests, total_tests):
        """Foydalanuvchining yechim natijalarini saqlash yoki yangilash"""
        solution, created = cls.objects.get_or_create(user=user, problem=problem, language=language)
        solution.code = code
        solution.execution_time = execution_time
        solution.memory_usage = memory_usage  # 🔥 RAM miqdorini saqlaymiz
        solution.passed_tests = passed_tests
        solution.total_tests = total_tests
        solution.is_accepted = passed_tests == total_tests  # Barcha testlardan o'tsa, qabul qilingan deb belgilash
        solution.calculate_score()  # Baholash tizimini ishga tushirish
        solution.save()
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
    def log_answer(cls, user, question, is_correct):
        """Foydalanuvchining savolga bergan javob natijasini saqlash"""
        result, created = cls.objects.get_or_create(user=user, question=question)
        result.is_correct = is_correct
        result.save()
        return result
