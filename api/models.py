from django.contrib.auth.models import User
from django.db import models
from django.db.models import signals
from django.dispatch import receiver


class Problem(models.Model):
    class Status(models.TextChoices):
        OPEN = 'O', 'Открыта'
        AGENT_REPLY_PROCESS = 'ARP', 'Ожидание ответа'
        RESOLVING = 'R', 'Проблема решается'
        CLOSED = 'C', 'Закрыта'

    author = models.ForeignKey(verbose_name='автор',
                               to=User,
                               on_delete=models.CASCADE)
    title = models.CharField(verbose_name='заголовок',
                             max_length=100)
    description = models.TextField(verbose_name='описание проблемы',
                                   max_length=10000)
    status = models.CharField(verbose_name='статус',
                              max_length=5,
                              choices=Status.choices,
                              default=Status.OPEN)

    created_at = models.DateTimeField(verbose_name='дата создания',
                                      auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='дата обновление',
                                      auto_now=True)

    class Meta:
        verbose_name = 'проблема'
        verbose_name_plural = 'проблемы'


class Message(models.Model):
    author = models.ForeignKey(verbose_name='автор',
                               to=User,
                               on_delete=models.CASCADE)
    text = models.TextField(verbose_name='описание проблемы',
                            max_length=10000)
    is_read = models.BooleanField(verbose_name='прочитано',
                                  default=False)

    created_at = models.DateTimeField(verbose_name='дата создания',
                                      auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='дата обновление',
                                      auto_now=True)

    class Meta:
        verbose_name = 'сообщение'
        verbose_name_plural = 'сообщения'


class Dormitory(models.Model):
    name = models.CharField(verbose_name='имя общежития',
                            max_length=200)
    address = models.CharField(verbose_name='адрес',
                               max_length=500)

    class Meta:
        verbose_name = 'общежитие'
        verbose_name_plural = 'общежития'


class Profile(models.Model):
    user = models.OneToOneField(verbose_name='пользователь',
                                to=User,
                                on_delete=models.CASCADE)
    dormitory = models.ForeignKey(verbose_name='общежитие',
                                  to=Dormitory,
                                  null=True,
                                  blank=True,
                                  on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'профиль'
        verbose_name_plural = 'профили'


@receiver(signals.post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(signals.post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
