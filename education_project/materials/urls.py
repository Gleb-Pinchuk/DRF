from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'courses', views.CourseViewSet)

urlpatterns = [
    path('lessons/', views.LessonListView.as_view()),
    path('lessons/<int:pk>/', views.LessonDetailView.as_view()),
]

urlpatterns += router.urls
