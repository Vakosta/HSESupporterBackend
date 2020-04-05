# Generated by Django 3.0.4 on 2020-04-05 18:26

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('api', '0010_message_is_from_student'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='dormitory',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE,
                                    related_name='messages', to='api.Dormitory', verbose_name='общежитие'),
        ),
    ]