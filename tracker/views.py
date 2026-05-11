from rest_framework import viewsets
from tracker.models import Habit
from tracker.pagination import MyPagination
from tracker.permissions import IsOwner, IsPublic
from rest_framework.permissions import AllowAny
from tracker.serializers import HabitSerializer
from rest_framework.decorators import action
from rest_framework.response import Response


class HabitViewSet(viewsets.ModelViewSet):
    """
    Представление для работы с привычками (CRUD операции).
    """
    pagination_class = MyPagination
    queryset = Habit.objects.all()
    serializer_class = HabitSerializer

    def get_queryset(self):
        if self.action == 'public':
            return Habit.objects.filter(is_public=True)

        return Habit.objects.filter(owner=self.request.user)

    def get_permissions(self):
        if self.action in ['update', 'destroy']:
            self.permission_classes = [IsOwner]
        elif self.action == 'retrieve':
            self.permission_classes = [IsPublic]
        elif self.action == 'public':
            self.permission_classes = [AllowAny]
        return [permission() for permission in self.permission_classes]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    @action(detail=False, methods=['get'], permission_classes=[])
    def public(self, request):
        queryset = Habit.objects.filter(is_public=True)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
