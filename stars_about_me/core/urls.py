from django.urls import path

from stars_about_me.core.views import QRCodeDetailView

urlpatterns = [
    path('luckies/<str:qr_id>/', QRCodeDetailView.as_view(), name='qr_code_detail'),
    path('luckies/<str:qr_id>/', QRCodeDetailView.as_view(), name='get_lucky'),
]