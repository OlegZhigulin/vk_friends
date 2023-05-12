from django.contrib.auth import get_user_model
from rest_framework import serializers

from api.models import Invate, Subscribe


User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        ref_name = 'MyUserSerializer'
        model = User
        fields = ('id', 'username',)


class InvateSerializers(serializers.ModelSerializer):
    sender_username = serializers.StringRelatedField(
        read_only=True, source='sender')

    class Meta:
        model = Invate
        fields = ('id', 'created', 'sender', 'sender_username')


class InvateCreateSerializers(serializers.ModelSerializer):
    class Meta:
        model = Invate
        fields = '__all__'


class InvateAcceptSerializers(serializers.ModelSerializer):
    class Meta:
        model = Subscribe
        fields = '__all__'
