from django.test import TestCase

# Create your tests here.
from django.test import TestCase
from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Course, Lesson

User = get_user_model()


class MaterialsTestCase(APITestCase):


    def setUp(self):
        self.user = User.objects.create_user(email='user@test.com', password='pass123')
        self.course = Course.objects.create(
            title='Курс',
            description='Описание',
            owner=self.user
        )


    def test_rutube_ru_allowed(self):
        """Rutube.ru — разрешён"""
        self.client.force_authenticate(user=self.user)
        data = {
            'title': 'Урок на Rutube',
            'course': self.course.id,
            'video_url': 'https://rutube.ru/video/12345/'
        }
        response = self.client.post('/api/lessons/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


    def test_rutube_com_allowed(self):
        """Rutube.com — разрешён"""
        self.client.force_authenticate(user=self.user)
        data = {
            'title': 'Урок на Rutube.com',
            'course': self.course.id,
            'video_url': 'https://rutube.com/watch?v=xyz'
        }
        response = self.client.post('/api/lessons/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


    def test_youtube_com_blocked(self):
        """YouTube.com — запрещён"""
        self.client.force_authenticate(user=self.user)
        data = {
            'title': 'Урок на YouTube',
            'course': self.course.id,
            'video_url': 'https://www.youtube.com/watch?v=abc123'
        }
        response = self.client.post('/api/lessons/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('video_url', response.data)


    def test_youtu_be_blocked(self):
        """Youtu.be — запрещён"""
        self.client.force_authenticate(user=self.user)
        data = {
            'title': 'Короткая ссылка YouTube',
            'course': self.course.id,
            'video_url': 'https://youtu.be/xyz789'
        }
        response = self.client.post('/api/lessons/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('video_url', response.data)


    def test_other_site_blocked(self):
        """Другие сайты (например, vimeo.com) — запрещены"""
        self.client.force_authenticate(user=self.user)
        data = {
            'title': 'Урок на Vimeo',
            'course': self.course.id,
            'video_url': 'https://vimeo.com/123456'
        }
        response = self.client.post('/api/lessons/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('video_url', response.data)


    def test_empty_video_url_allowed(self):
        """Пустая ссылка — разрешена"""
        self.client.force_authenticate(user=self.user)
        data = {
            'title': 'Урок без видео',
            'course': self.course.id,
            'video_url': ''
        }
        response = self.client.post('/api/lessons/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
