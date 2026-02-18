from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.CreatePaymentView.as_view(), name='create_payment'),
    path('status/<str:session_id>/', views.CheckPaymentStatusView.as_view(), name='payment_status'),
]
