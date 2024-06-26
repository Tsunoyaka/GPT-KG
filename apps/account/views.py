from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from django.contrib.auth import get_user_model
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from .serializers import (
    UserRegistrationSerializer, 
    PasswordChangeSerializer,
    RestorePasswordSerializer,
    SetRestoredPasswordSerializer,
    UsersSerializer
    )
from apps.chat.models import Chat

User = get_user_model()


class RegistrationView(APIView):
    @swagger_auto_schema(request_body=UserRegistrationSerializer)
    def post(self, request: Request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(
                'Спасибо за регистрацию!',
                status=status.HTTP_201_CREATED
            )

class AccountActivationView(APIView):
    def get(self, request, activation_code):
        user = User.objects.filter(activation_code=activation_code).first()
        if not user:
            return Response(
                'Страница не найдена...', 
                status=status.HTTP_404_NOT_FOUND
                )
        user.is_active = True
        user.activation_code = ''
        user.save()
        return Response(
            'Учетная запись активирована! Теперь Вы можете войти на Booking.com', 
            status=status.HTTP_200_OK
            )


class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request: Request):
        serializer = PasswordChangeSerializer(data=request.data, context={'request': request})
        if serializer.is_valid(raise_exception=True):
            serializer.set_new_password()
            return Response(
                'Ваш пароль успешно изменен.',
                status=status.HTTP_200_OK
            )


class RestorePasswordView(APIView):
    def post(self, request: Request):
        serializer = RestorePasswordSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.send_code()
            return Response(
                'Код для восстановления пароля был отправлен Вам на почту.',
                status=status.HTTP_200_OK
            )


class SetRestoredPasswordView(APIView):
    def post(self, request: Request):
        serializer = SetRestoredPasswordSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.set_new_password()
            return Response(
                'Ваш пароль успешно восстановлен.',
                status=status.HTTP_200_OK
            )


class DeleteAccountView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request: Request):
        username = request.user.username
        User.objects.get(username=username).delete()
        return Response(
            'Учетная запись удалена.',
            status=status.HTTP_204_NO_CONTENT
        )

class MyChats(APIView):
    def post(self, request):
        user = request.user
        chats = Chat.objects.filter(user=user)
        list_ = []
        if chats.exists():
            for chat in chats:
                dict_ = {
                    "id": chat.id,
                    "title": chat.title,
                    "user": chat.user.email
                }
                print(dict_)
                list_.append(dict_)
            return Response(list_)
        return 'У данного пользователя нет чатов'