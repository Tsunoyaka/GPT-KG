# Generated by Django 5.0.4 on 2024-04-16 18:28

import apps.chat.validates
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='audio',
            name='text',
            field=models.CharField(blank=True, max_length=4096, null=True, verbose_name='Аудио в текст'),
        ),
        migrations.AlterField(
            model_name='audio',
            name='audio',
            field=models.FileField(upload_to='Audio', validators=[apps.chat.validates.validate_mp3]),
        ),
        migrations.AlterField(
            model_name='video',
            name='video',
            field=models.FileField(default=django.utils.timezone.now, upload_to='Video', validators=[apps.chat.validates.validate_mp4]),
            preserve_default=False,
        ),
    ]