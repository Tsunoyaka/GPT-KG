from django.db import models
from django.core.exceptions import ValidationError
from .validates import validate_mp3, validate_mp4


class Chat(models.Model):
    title = models.CharField(verbose_name='Название', max_length=50)
    user = models.ForeignKey(
        to='account.User',
        on_delete=models.CASCADE,
        related_name='user_chat'
        )

    def __str__(self) -> str:
        return self.title


class Message(models.Model):
    chat = models.ForeignKey(to=Chat, on_delete=models.CASCADE, related_name='chat_message')
    message = models.CharField(verbose_name='Сообщение', max_length=4096)
    created_at = models.DateTimeField(verbose_name='Дата создания', auto_now_add=True)
    user = models.ForeignKey(
        to='account.User',
        on_delete=models.CASCADE,
        related_name='user_message'
        )

    def clean(self):
        if not self.message and not self.file:
            raise ValidationError('Сообщение или файл должны быть заполнены.')

    def save(self, *args, **kwargs):
        self.full_clean() 
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.message


class Audio(models.Model):
    chat = models.ForeignKey(to=Chat, on_delete=models.CASCADE, related_name='audio_message')
    audio = models.FileField(upload_to='Audio', validators=[validate_mp3])
    text = models.CharField(verbose_name='Аудио в текст', max_length=4096, blank=True, null=True)
    created_at = models.DateTimeField(verbose_name='Дата создания', auto_now_add=True)
    user = models.ForeignKey(
        to='account.User',
        on_delete=models.CASCADE,
        related_name='user_audio'
        )   


class Video(models.Model):
    chat = models.ForeignKey(to=Chat, on_delete=models.CASCADE, related_name='video_message')
    video = models.FileField(upload_to='Video', validators=[validate_mp4])
    created_at = models.DateTimeField(verbose_name='Дата создания', auto_now_add=True)
    user = models.ForeignKey(
        to='account.User',
        on_delete=models.CASCADE,
        related_name='user_video'
        )


class Docx(models.Model):
    chat = models.ForeignKey(to=Chat, on_delete=models.CASCADE, related_name='docx_message')
    docx = models.FileField(upload_to='Docx')
    created_at = models.DateTimeField(verbose_name='Дата создания', auto_now_add=True)
    user = models.ForeignKey(
        to='account.User',
        on_delete=models.CASCADE,
        related_name='user_docx'
        )

class Photo(models.Model):
    chat = models.ForeignKey(to=Chat, on_delete=models.CASCADE, related_name='photo_message')
    photo = models.FileField(upload_to='Photo')
    created_at = models.DateTimeField(verbose_name='Дата создания', auto_now_add=True)
    user = models.ForeignKey(
        to='account.User',
        on_delete=models.CASCADE,
        related_name='user_photo'
        )
