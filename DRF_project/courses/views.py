from drf_spectacular.utils import extend_schema
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import Course
from .serializers import CourseSerializer


@extend_schema(
    tags=['courses'],
    summary='Получить список курсов',
    description='Возвращает пагинированный список доступных курсов',
)
class CourseViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet для просмотра курсов.
    """
    queryset = Course.objects.filter(is_published=True)
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
