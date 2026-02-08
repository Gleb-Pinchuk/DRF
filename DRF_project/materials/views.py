from rest_framework import viewsets, generics
from rest_framework.permissions import BasePermission, IsAuthenticated
from django.core.exceptions import PermissionDenied
from .models import Course, Lesson
from .serializers import CourseSerializer, LessonSerializer
from users.permissions import IsModerator

class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user

class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.action in ['create', 'destroy']:
            self.permission_classes = [IsAuthenticated]
        elif self.action in ['update', 'partial_update']:
            self.permission_classes = [IsAuthenticated]
        elif self.action in ['list', 'retrieve']:
            self.permission_classes = [IsAuthenticated]
        return [permission() for permission in self.permission_classes]

    def get_queryset(self):
        if IsModerator().has_permission(self.request, self):
            return Course.objects.all()
        return Course.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def destroy(self, request, *args, **kwargs):
        course = self.get_object()
        if course.owner != request.user:
            raise PermissionDenied("Вы не можете удалить чужой курс")
        return super().destroy(request, *args, **kwargs)

class LessonListView(generics.ListCreateAPIView):
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if IsModerator().has_permission(self.request, self):
            return Lesson.objects.all()
        return Lesson.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class LessonDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if IsModerator().has_permission(self.request, self):
            return Lesson.objects.all()
        return Lesson.objects.filter(owner=self.request.user)

    def delete(self, request, *args, **kwargs):
        lesson = self.get_object()
        if lesson.owner != request.user:
            raise PermissionDenied("Вы не можете удалить чужой урок")
        return super().delete(request, *args, **kwargs)
