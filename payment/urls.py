from django.urls import path
from .views import CreatePaymentAPIView, stripe_webhook

urlpatterns = [
    path('create/<int:borrowing_id>/', CreatePaymentAPIView.as_view(), name="create_payment"),
    path('webhook/', stripe_webhook, name="stripe_webhook"),
]
