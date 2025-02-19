from django.db.models.signals import post_save
from django.dispatch import receiver
from userstatus.models import UserLeaderboard, UserProblemStatus
from .models import Solution

@receiver(post_save, sender=Solution)
def update_user_problem_status(sender, instance, **kwargs):
    if instance.is_accepted:
        if not UserProblemStatus.objects.filter(user=instance.user, problem=instance.problem, is_completed=True).exists():
            UserProblemStatus.mark_completed(instance.user, instance.problem, instance.difficulty)
            UserLeaderboard.update_leaderboard()

