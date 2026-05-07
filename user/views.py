from rest_framework.generics import CreateAPIView

from user.models import CustomUser
from user.serializers import RegisterSerializer
from rest_framework.permissions import AllowAny


class RegisterView(CreateAPIView):
    """
        Представление для регистрации.
    """
    queryset = CustomUser.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]
