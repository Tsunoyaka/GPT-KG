from django.contrib import admin
from .models import Chat, Message, Audio, Video

admin.site.register(Chat)
admin.site.register(Message)
admin.site.register(Audio)
admin.site.register(Video)