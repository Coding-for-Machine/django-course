from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Profile, MyUser

@receiver(post_save, sender=MyUser)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        # Profil yaratish
        Profile.objects.create(
            user=instance,
            first_name=instance.first_name or '',
            last_name=instance.last_name or ''
        )
    else:
        # Profilni yangilash
        profile, _ = Profile.objects.get_or_create(user=instance)
        profile.first_name = instance.first_name
        profile.last_name = instance.last_name
        profile.save()

            
@receiver(post_save, sender=MyUser)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()