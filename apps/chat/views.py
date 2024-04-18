from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from .models import Chat, Message, Audio, Video, Docx, Photo
from .serializers import (
    ChatSerializer, 
    MessageSerializer, 
    AudioSerializer, 
    VideoSerializer,
    DocxSerializer,
    PhotoSerializer
    )
from .gemini import gemimi_answer
from .utils import (
    audio_to_text, 
    download_audio_as_wav, 
    split_and_recognize, 
    process_video_and_recognize_text,
    translate_text,
    audio_kg,
    audio_split_kg,
    text_to_audio
    )
from .validates import is_youtube_link, is_string
import os
from docx2pdf import convert


User = get_user_model()

class ChatViewSet(ModelViewSet):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer


class MessageViewSet(ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    

    def create(self, request, *args, **kwargs):
        super().create(request, *args, **kwargs)
        message = request.data.get('message')
        kg_ru = translate_text(text=message, src_lang='ky', dest_lang='ru')
        chat_id = request.data.get('chat')
        chat = Chat.objects.get(id=chat_id)
        gemini = User.objects.get(email='gemini@gemini.com')
        if not is_youtube_link(message):
            answer = gemimi_answer(kg_ru)
            ru_kg = translate_text(text=answer, src_lang='ru', dest_lang='ky')
            model = Message.objects.create(user=gemini, chat=chat, message=ru_kg)
            model.save()
            return Response(ru_kg)   
        language = request.data.get('language')
        wav_audio = download_audio_as_wav(message)
        print('Ссылка рабочая')
        if is_string(wav_audio):
            return Response(wav_audio)
        text_ = split_and_recognize(wav_audio, language)
        answer = gemimi_answer("Сделай короткий пересказ со смыслом этого текста: " + text_)
        ru_kg = translate_text(text=answer, src_lang='ru', dest_lang='ky')
        model = Message.objects.create(user=gemini, chat=chat, message=ru_kg)
        model.save()  
        return Response(ru_kg)   



class AudioViewSet(ModelViewSet):
    queryset = Audio.objects.all()
    serializer_class = AudioSerializer

    def create(self, request, *args, **kwargs):
        audio_file = request.FILES.get('audio')
        kg_text = audio_kg(audio_file=audio_file)
        kg_ru = translate_text(text=kg_text, src_lang='ky', dest_lang='ru')
        chat_id = request.data.get('chat')
        chat = Chat.objects.get(id=chat_id)
        g_answer = gemimi_answer(kg_ru)
        ru_kg = translate_text(text=g_answer, src_lang='ru', dest_lang='ky')
        gemini = User.objects.get(email='gemini@gemini.com')
        super().create(request, *args, **kwargs)
        model = Message.objects.create(user=gemini, chat=chat, message=ru_kg)
        model.save()
        return Response(ru_kg)


class VideoViewSet(ModelViewSet):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer

    # def create(self, request, *args, **kwargs):
    #     super().create(request, *args, **kwargs)
    #     # video_name = request.data.get('video')
    #     # uploaded_file = request.FILES.get('video')

    #     # video_path = r"C:\Users\user\Desktop\hackathon\media\Video\Привет_я_Русский_оккупант__Патриотическое_видео.mp4"
    #     # print(video_name)
    #     # # Обработка видео и распознавание текста
    #     # recognized_text = process_video_and_recognize_text(video_path)
    #     # print("Распознанный текст:", recognized_text)
    #     return Response('none')
    

class AudioTextView(APIView):
    def post(self, request):
        chat_id = request.data.get('chat')
        audio_id = request.data.get('audio')
        chat = Chat.objects.get(id=chat_id)
        get_aud = Audio.objects.get(chat=chat, id=audio_id)
        message = audio_to_text(audio_file=get_aud.audio)
        get_aud.text = message
        get_aud.save()
        return Response(message)
    
    
class AudioToAudioView(APIView):
    def post(self, request):
        audio = request.data.get('audio')
        audio_to_text = audio_kg(audio)
        kg_ru = translate_text(text=audio_to_text, src_lang="ky", dest_lang="ru")
        gemini = gemimi_answer(kg_ru)
        audio_answer = text_to_audio(text=gemini)
        content_type = 'audio/mpeg'
        return Response(audio_answer, content_type=content_type)


class LinkView(APIView):
    def post(self, request):
        return Response('Видео кайсы тилде?')
    
    
class PhotoViewSet(ModelViewSet):
    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer
    
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)