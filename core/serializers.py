from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer ,UserSerializer as BaseUserSerializer
from django.conf import settings



# we need to register this serializer in settings.py
class UserCreateSerializer(BaseUserCreateSerializer):


    class Meta(BaseUserCreateSerializer.Meta):
        Model : settings.AUTH_USER_MODEL
        fields = ['id', 'email', 'username', 'password', 'first_name', 'last_name']

class UserSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
        Model : settings.AUTH_USER_MODEL
        fields = ['id', 'email', 'username', 'first_name', 'last_name']