# Generated by Django 3.0.2 on 2020-01-12 16:50

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Problem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='заголовок')),
                ('description', models.TextField(max_length=10000, verbose_name='описание проблемы')),
                ('status', models.CharField(
                    choices=[('O', 'Открыта'), ('ARP', 'Ожидание ответа'), ('R', 'Проблема решается'),
                             ('C', 'Закрыта')], default='O', max_length=5, verbose_name='статус')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='дата создания')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='дата обновление')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL,
                                             verbose_name='автор')),
            ],
            options={
                'verbose_name': 'проблема',
                'verbose_name_plural': 'проблемы',
            },
        ),
    ]