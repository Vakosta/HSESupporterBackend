from django.contrib.auth.models import User
from django.db import models
from django.db.models import signals
from django.dispatch import receiver


class Dormitory(models.Model):
    name = models.CharField(verbose_name='имя общежития',
                            max_length=200)
    address = models.CharField(verbose_name='адрес',
                               max_length=500)

    class Meta:
        verbose_name = 'общежитие'
        verbose_name_plural = 'общежития'

    def __str__(self):
        return self.name


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
        verbose_name = 'обращение'
        verbose_name_plural = 'обращения'

    def __str__(self):
        return '{}: {}'.format(self.author, self.title[:17])


class Message(models.Model):
    author = models.ForeignKey(verbose_name='автор',
                               to=User,
                               on_delete=models.CASCADE)
    text = models.TextField(verbose_name='описание проблемы',
                            max_length=10000)
    is_read = models.BooleanField(verbose_name='прочитано',
                                  default=False)
    is_from_student = models.BooleanField(verbose_name='от студента ли',
                                          default=True)
    problem = models.ForeignKey(verbose_name='обращение',
                                to=Problem,
                                null=True,
                                related_name='messages',
                                blank=True,
                                on_delete=models.CASCADE)
    dormitory = models.ForeignKey(verbose_name='общежитие',
                                  to=Dormitory,
                                  null=True,
                                  related_name='messages',
                                  blank=True,
                                  on_delete=models.CASCADE)

    created_at = models.DateTimeField(verbose_name='дата создания',
                                      auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='дата обновление',
                                      auto_now=True)

    class Meta:
        verbose_name = 'сообщение'
        verbose_name_plural = 'сообщения'

    def __str__(self):
        return '{}: {}'.format(self.author, self.text[:17])


class Notice(models.Model):
    main_text = models.CharField(verbose_name='главный текст',
                                 max_length=200)
    text = models.TextField(verbose_name='текст',
                            max_length=10000)
    is_important = models.BooleanField(verbose_name='важное ли',
                                       default=False)

    created_at = models.DateTimeField(verbose_name='дата создания',
                                      auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='дата обновление',
                                      auto_now=True)

    class Meta:
        verbose_name = 'объявление'
        verbose_name_plural = 'объявления'

    def __str__(self):
        return '{}'.format(self.main_text[:25])


class Profile(models.Model):
    user = models.OneToOneField(verbose_name='пользователь',
                                to=User,
                                on_delete=models.CASCADE)
    dormitory = models.ForeignKey(verbose_name='общежитие',
                                  to=Dormitory,
                                  null=True,
                                  blank=True,
                                  on_delete=models.CASCADE)

    is_login = models.BooleanField(verbose_name='был ли первый вход',
                                   default=False)
    is_accept = models.BooleanField(verbose_name='подтверждён ли администратором',
                                    default=False)

    class Meta:
        verbose_name = 'профиль'
        verbose_name_plural = 'профили'

    def __str__(self):
        return self.user.email


class Confirmation(models.Model):
    email = models.CharField(verbose_name='Email',
                             max_length=40)
    code = models.CharField(verbose_name='код подтверждения',
                            max_length=10)

    class Meta:
        verbose_name = 'подтверждение'
        verbose_name_plural = 'подтверждения'

    def __str__(self):
        return '{} — {}'.format(self.email, self.code)


@receiver(signals.post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(signals.post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
