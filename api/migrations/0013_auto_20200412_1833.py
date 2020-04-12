# Generated by Django 3.0.5 on 2020-04-12 15:33

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('api', '0012_confirmation'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='is_accept',
            field=models.BooleanField(default=False, verbose_name='подтверждён ли администратором'),
        ),
        migrations.AddField(
            model_name='profile',
            name='is_login',
            field=models.BooleanField(default=False, verbose_name='был ли первый вход'),
        ),
    ]