from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from api.models import Invate, Subscribe
from api.serializers import (
    InvateAcceptSerializers,
    InvateCreateSerializers,
    InvateSerializers,
    UserSerializer,
)


User = get_user_model()


class FriendList(generics.ListAPIView):
    serializer_class = UserSerializer

    def get_queryset(self):
        user = self.request.user
        queryset = user.you_friends.all()
        return queryset


class InvateList(generics.ListAPIView):
    serializer_class = InvateSerializers

    def get_queryset(self):
        user = self.request.user
        queryset = Invate.objects.filter(receiver=user)
        return queryset


class InvateCreate(generics.CreateAPIView):
    serializer_class = InvateCreateSerializers

    def create(self, request, *args, **kwargs):
        to_user_id = kwargs.get('user_id', None)
        if to_user_id:
            try:
                to_user = User.objects.get(id=to_user_id)
            except User.DoesNotExist:
                return Response(
                    'Такого пользователя не существует',
                    status=status.HTTP_404_NOT_FOUND,
                )
            if to_user != request.user:
                try:
                    friend_request = Invate.objects.create(
                        sender=request.user,
                        receiver=to_user,
                    )
                except IntegrityError:
                    return Response(
                        'Вы уже отправили заявку',
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    )
                serializer = self.get_serializer(friend_request)
                return Response(
                    serializer.data,
                    status=status.HTTP_201_CREATED,
                )
            return Response(
                'Самому себе нельзя отправить дружбу',
                status=status.HTTP_400_BAD_REQUEST,
            )


class InvateAccept(generics.CreateAPIView):
    serializer_class = InvateAcceptSerializers

    def create(self, request, *args, **kwargs):
        id_invate = kwargs.get('id_invate', None)
        if id_invate:
            try:
                invate = Invate.objects.get(id=id_invate)
            except Invate.DoesNotExist:
                return Response(
                    'Такой заявки не существует',
                    status=status.HTTP_404_NOT_FOUND,
                )
            try:
                from_user = User.objects.get(id=invate.receiver.id)
                to_user = User.objects.get(id=invate.sender.id)
            except User.DoesNotExist:
                return Response(
                    'Такого пользователя не существует',
                    status=status.HTTP_404_NOT_FOUND,
                )
            if to_user != request.user:
                try:
                    friend_request = Subscribe.objects.create(
                        author=from_user,
                        user=to_user,
                    )
                except IntegrityError:
                    return Response(
                        'Вы уже в друзьях',
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    )
                serializer = self.get_serializer(friend_request)
                invate.delete()
                return Response(
                    serializer.data,
                    status=status.HTTP_201_CREATED,
                )
            return Response(
                'Самому себе нельзя отправить дружбу',
                status=status.HTTP_400_BAD_REQUEST,
            )


class InvateDelete(generics.DestroyAPIView):
    serializer_class = InvateSerializers
    queryset = Invate.objects.all()


@api_view(['DELETE'])
def delete_friend(request, *args, **kwargs):
    id_friend = kwargs.get('id_friend', None)
    if id_friend:
        try:
            friend = User.objects.get(id=id_friend)
        except User.DoesNotExist:
            return Response(
                'Такого пользователя не существует',
                status=status.HTTP_404_NOT_FOUND,
            )
    subscribe = Subscribe.objects.filter(
        user=friend, author=request.user).first()
    if subscribe:
        subscribe.delete()
        return Response(
            status=status.HTTP_204_NO_CONTENT,
        )
    return Response(
        'А у Вас такого друга и не было',
        status=status.HTTP_404_NOT_FOUND,
    )


@api_view(['GET'])
def check_status_relationship(request, *args, **kwargs):
    user_id = kwargs.get('user_id', None)
    if user_id:
        try:
            with_user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response(
                'Такого пользователя не существует',
                status=status.HTTP_404_NOT_FOUND,
            )
        is_friend = Subscribe.objects.filter(
            author=request.user, user=with_user).exists()
        if is_friend:
            return Response(
                f'{with_user.username} это Ваш друг',
                status=status.HTTP_200_OK,
            )
        is_send_invate = Invate.objects.filter(
            sender=request.user, receiver=with_user).first()
        if is_send_invate:
            return Response(
                f'У вас есть входящая заявка от {with_user.username}',
                status=status.HTTP_200_OK,
            )
        is_recv_invate = Invate.objects.filter(
            sender=with_user, receiver=request.user).first()
        if is_recv_invate:
            return Response(
                f'Вы отправили заявку {with_user.username}',
                status=status.HTTP_200_OK,
            )
        return Response(
            f'У Вас нет ничего общего с {with_user.username}',
            status=status.HTTP_200_OK,
        )
