from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from .models import Chat, Message, Audio, Video
from .serializers import ChatSerializer, MessageSerializer, AudioSerializer, VideoSerializer
from .gemini import gemimi_answer

class ChatViewSet(ModelViewSet):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer


class MessageViewSet(ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer


    def create(self, request, *args, **kwargs):
        super().create(request, *args, **kwargs)
        message = request.data['message']
        answer = gemimi_answer(message)
        chat_id = request.data['chat']
        chat = Chat.objects.get(id=chat_id)
        model = Message.objects.create(chat=chat, message=answer)
        model.save()
        return Response(answer)


class AudioViewSet(ModelViewSet):
    queryset = Audio.objects.all()
    serializer_class = AudioSerializer


class VideoViewSet(ModelViewSet):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer
