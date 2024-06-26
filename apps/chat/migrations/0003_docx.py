# Generated by Django 5.0.4 on 2024-04-17 21:57

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0002_audio_text_alter_audio_audio_alter_video_video'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Docx',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('docx', models.FileField(upload_to='Docx')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('chat', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='docx_message', to='chat.chat')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_docx', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
