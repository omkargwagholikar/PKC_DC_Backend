from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from ..models import *


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        custom_user = CustomUser.objects.get(user=user)

        token["user_name"] = user.username
        token["is_judge"] = custom_user.is_judge
        token["is_player"] = custom_user.is_player

        return token
