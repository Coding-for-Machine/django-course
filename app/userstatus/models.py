from django.db import models
from django.utils import timezone
from users.models import MyUser  # Foydalanuvchi modeli
from lessons.models import Lesson, Problem
from solution.models import Solution, UserQuizResult

# ==========================
# 1. UserActivity modeli - Foydalanuvchi faoliyatini saqlash
# ==========================

class UserActivityDaily(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='daily_activities')
    date = models.DateField(default=timezone.now)  # Foydalanuvchi harakat qilgan sana
    activity_count = models.PositiveIntegerField(default=0)  # Nechta faoliyat bajargani
    total_duration = models.PositiveIntegerField(default=0)  # Umumiy shug‘ullanish vaqti (daqiqalarda)
    score = models.PositiveIntegerField(default=0)  # Ball

    class Meta:
        unique_together = ('user', 'date')  # Har kuni faqat bitta yozuv bo'lishi kerak
        ordering = ['-date']
        verbose_name = "User Daily Activity"
        verbose_name_plural = "User Daily Activities"

    def __str__(self):
        return f"{self.user.email} - {self.date}: {self.activity_count} actions, {self.score} points"

    @classmethod
    def log_activity(cls, user, activity_count=1, duration=0, score=0):
        """Foydalanuvchi harakatini qo‘shish yoki yangilash"""
        today = timezone.now().date()
        activity, created = cls.objects.get_or_create(user=user, date=today)
        activity.activity_count += activity_count  # Kiritilgan harakatlar sonini qo‘shish
        activity.total_duration += duration  # Vaqtni qo‘shish
        activity.score += score  # Ballni qo‘shish
        activity.save()
        return activity
    
class Badge(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    icon = models.ImageField(upload_to="badges/")  # Nishon rasmi

    def __str__(self):
        return self.name


class UserBadge(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    badge = models.ForeignKey(Badge, on_delete=models.CASCADE)
    date_earned = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email} - {self.badge.name}"

class UserActivitySummary(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    period_type = models.CharField(
        max_length=10,
        choices=[('weekly', 'Weekly'), ('monthly', 'Monthly')]
    )
    period_start = models.DateField()  # Boshlanish sanasi
    period_end = models.DateField()  # Tugash sanasi
    total_score = models.PositiveIntegerField(default=0)  # Umumiy ball
    total_activity = models.PositiveIntegerField(default=0)  # Faoliyatlar soni

    class Meta:
        unique_together = ('user', 'period_type', 'period_start')

    def __str__(self):
        return f"{self.user.email} - {self.period_type}: {self.total_score} points"

class UserLeaderboard(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    total_score = models.PositiveIntegerField(default=0)  # Jami ball
    last_updated = models.DateTimeField(auto_now=True)

    @classmethod
    def update_leaderboard(cls):
        """Foydalanuvchilar reytingini yangilash"""
        users = MyUser.objects.all()
        for user in users:
            quiz_score = UserQuizResult.objects.filter(user=user).aggregate(models.Sum('score'))['score__sum'] or 0
            activity_score = UserActivityDaily.objects.filter(user=user).aggregate(models.Sum('score'))['score__sum'] or 0
            problem_score = UserProblemStatus.objects.filter(user=user).aggregate(models.Sum('score'))['score__sum'] or 0
            solution_score = Solution.objects.filter(user=user).aggregate(models.Sum('score'))['score__sum'] or 0  # ✅ Solution ballari qo'shildi

            total_score = quiz_score + activity_score + problem_score + solution_score
            leaderboard, created = cls.objects.get_or_create(user=user)
            leaderboard.total_score = total_score
            leaderboard.save()


# ==========================
# 2. UserLessonStatus modeli - Foydalanuvchining dars holati
# ==========================
class UserLessonStatus(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    is_completed = models.BooleanField(default=False)  # Dars tugallandimi?
    progress = models.PositiveIntegerField(default=0)  # Darsdagi progress (foizlarda)

    def __str__(self):
        return f"User: {self.user.email}, Lesson: {self.lesson.title}, Completed: {self.is_completed}"

    def update_progress(self, completed_parts, total_parts):
        """Darsdagi progressni aniq hisoblash"""
        if self.is_completed:
            self.progress = 100
        else:
            self.progress = min(int((completed_parts / total_parts) * 100), 100)
        self.save()

# ==========================
# 3. UserProblemStatus modeli - Foydalanuvchining problem holati
# ==========================
class UserProblemStatus(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    is_completed = models.BooleanField(default=False)  # Muammo yechimi tugallandimi?
    score = models.PositiveIntegerField(default=0)  # Ball

    def __str__(self):
        return f"User: {self.user.email}, Problem: {self.problem.title}, Completed: {self.is_completed}"

    def update_score(self, difficulty_level=1):
        """Muammo yechimi uchun ballni yangilash"""
        if self.is_completed:
            self.score = difficulty_level * 10  # Masalan, qiyinlik darajasiga ko‘ra ball
        else:
            self.score = 0
        self.save()



