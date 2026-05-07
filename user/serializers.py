from rest_framework import serializers
from .models import CustomUser

class RegisterSerializer(serializers.ModelSerializer):
    """Сериализатор для регистрации """
    class Meta:
        model = CustomUser
        fields = '__all__'

    def create(self, validated_data):
        user, created = CustomUser.objects.get_or_create(
            chat_id=validated_data['chat_id'],
        )
        return user