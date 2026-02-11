from rest_framework import viewsets, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.core.exceptions import PermissionDenied
from .models import Course, Lesson, Subscription
from .serializers import CourseSerializer, LessonSerializer
from .paginators import MaterialsPagination
from users.permissions import IsModerator


class IsOwner:
    def is_owner(self, obj, user):
        return obj.owner == user


class CourseViewSet(viewsets.ModelViewSet, IsOwner):
    queryset = Course.objects.all()  # ← ДОБАВЛЕНО: обязательно для роутера
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = MaterialsPagination

    def get_queryset(self):
        if IsModerator().has_permission(self.request, self):
            return Course.objects.all()
        return Course.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def destroy(self, request, *args, **kwargs):
        course = self.get_object()
        if not self.is_owner(course, request.user):
            raise PermissionDenied("Вы не можете удалить чужой курс")
        return super().destroy(request, *args, **kwargs)


class LessonListView(generics.ListCreateAPIView, IsOwner):
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = MaterialsPagination

    def get_queryset(self):
        if IsModerator().has_permission(self.request, self):
            return Lesson.objects.all()
        return Lesson.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class LessonDetailView(generics.RetrieveUpdateDestroyAPIView, IsOwner):
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if IsModerator().has_permission(self.request, self):
            return Lesson.objects.all()
        return Lesson.objects.filter(owner=self.request.user)

    def delete(self, request, *args, **kwargs):
        lesson = self.get_object()
        if not self.is_owner(lesson, request.user):
            raise PermissionDenied("Вы не можете удалить чужой урок")
        return super().delete(request, *args, **kwargs)


class SubscriptionView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user
        course_id = request.data.get('course_id')

        if not course_id:
            return Response({"error": "course_id обязателен"}, status=400)

        course = get_object_or_404(Course, id=course_id)
        subscription = Subscription.objects.filter(user=user, course=course)

        if subscription.exists():
            subscription.delete()
            message = "подписка удалена"
        else:
            Subscription.objects.create(user=user, course=course)
            message = "подписка добавлена"

        return Response({"message": message})
