from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny

from user.models import CustomUser
from user.serializers import RegisterSerializer


class RegisterView(CreateAPIView):
    """
        Представление для регистрации.
    """
    queryset = CustomUser.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]
