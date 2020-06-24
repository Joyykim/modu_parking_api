from .models import User
from rest_framework import serializers
from action_serializer import ModelActionSerializer


class UserSerializer(ModelActionSerializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    points = serializers.ReadOnlyField()
    created = serializers.ReadOnlyField()

    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'password', 'phoneNum', 'plateNum', 'cardNum', 'points', 'created')
        action_fields = {
            'login': {'fields': ('email', 'password', 'username'), 'read_only_fields': ('username',)},
            'update': {'fields': ('email', 'username')},
        }

    def create(self, validated_data):
        user = super(UserSerializer, self).create(validated_data)
        if 'password' in validated_data:
            user.set_password(validated_data['password'])
            user.save()
        return user
