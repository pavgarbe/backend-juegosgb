from django.urls import path
from .views import *

app_name = 'karaoke'

urlpatterns = [
    path('canciones/', CancionAPIView.as_view(), name='cancion-list'),
    path('canciones/upload/', UploadCanciones.as_view(), name='upload-canciones'),
]