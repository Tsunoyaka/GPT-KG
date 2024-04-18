from rest_framework import serializers
from .models import Chat, Message, Audio, Video, Docx, Photo
from .validates import check_path

class ChatSerializer(serializers.ModelSerializer):  
    user = serializers.ReadOnlyField(
        source='user.username'
    )
    
    class Meta:
        model = Chat
        fields = ['id', 'title', 'user']

    def validate(self, attrs):
        user = self.context.get('request').user
        attrs['user'] = user
        return attrs

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        context = self.context
        request = context.get('request')
        request_path = request.path
        if request.method == 'GET' and check_path(request_path):
            messages = Message.objects.filter(chat=instance)
            audios = Audio.objects.filter(chat=instance)
            videos = Video.objects.filter(chat=instance)

            all_content = list(messages) + list(audios) + list(videos)
            all_content.sort(key=lambda x: x.created_at)

            serialized_content = []
            for content in all_content:
                if isinstance(content, Message):
                    serialized_content.append(MessageSerializer(content).data)
                elif isinstance(content, Audio):
                    serialized_content.append(AudioSerializer(content).data)
                elif isinstance(content, Video):
                    serialized_content.append(VideoSerializer(content).data)

            representation['chat_content'] = serialized_content
            return representation
        return {
                'id': instance.id,
                'title': instance.title
            }
   
    

class MessageSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(
        source='user.username'
    )
    
    class Meta:
        model = Message
        fields = ['id', 'chat', 'message', 'created_at', 'user']

    def validate(self, attrs):
        user = self.context.get('request').user
        attrs['user'] = user
        return attrs


class AudioSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(
        source='user.username'
    )
    class Meta:
        model = Audio
        fields = ['id', 'chat', 'audio', 'created_at', 'user']

    def validate(self, attrs):
        user = self.context.get('request').user
        attrs['user'] = user
        return attrs


class VideoSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(
        source='user.username'
    )
    
    class Meta:
        model = Video
        fields = ['id', 'chat', 'video', 'created_at', 'user']

    def validate(self, attrs):
        user = self.context.get('request').user
        attrs['user'] = user
        return attrs

    def create(self, validated_data):
        print(validated_data)
        return super().create(validated_data)
 
 
class DocxSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(
        source='user.username'
    )
    class Meta:
        model = Docx
        fields = ['id', 'chat', 'docx', 'created_at', 'user']

    def validate(self, attrs):
        user = self.context.get('request').user
        attrs['user'] = user
        return attrs
    
 
class PhotoSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(
        source='user.username'
    )
    class Meta:
        model = Docx
        fields = ['id', 'chat', 'photo', 'created_at', 'user']

    def validate(self, attrs):
        user = self.context.get('request').user
        attrs['user'] = user
        return attrs