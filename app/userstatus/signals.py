
from django.dispatch import receiver
from django.db.models.signals import post_save
from solution.models import Solution, UserQuizResult
from userstatus.models import UserActivityDaily, UserLeaderboard, UserProblemStatus


@receiver(post_save, sender=UserQuizResult)
@receiver(post_save, sender=UserActivityDaily)
@receiver(post_save, sender=UserProblemStatus)
@receiver(post_save, sender=Solution)
def update_leaderboard_signal(sender, instance, **kwargs):
    UserLeaderboard.update_leaderboard(instance.user)