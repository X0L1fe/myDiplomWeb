from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import UserProfile, User

@receiver(post_save, sender=User)
def create_or_save_user_profile(sender, instance, created, **kwargs):
    if created:
        # Если пользователь создан, создаём связанный профиль
        UserProfile.objects.create(user=instance)
    else:
        # Если пользователь обновляется, сохраняем его профиль, если он существует
        if hasattr(instance, 'profile'):
            instance.profile.save()
