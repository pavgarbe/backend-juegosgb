from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import os
import json
import requests
from .models import Cancion
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import requests
from django.conf import settings

class CancionAPIView(APIView):
    def get(self, request, *args, **kwargs):
        canciones = Cancion.objects.all()
        data = [{"id": cancion.id, "nombre": cancion.nombre, "artista": cancion.artista, "genero": cancion.genero, "archivo": 'http://127.0.0.1:8000/media/karaoke/'+cancion.archivo} for cancion in canciones]
        return Response(data, status=status.HTTP_200_OK)


class UploadCanciones(APIView):
    def get(self, request):
        file = os.path.join(settings.BASE_DIR, 'apps/karaoke/canciones_karaoke.json')
        with open(file, 'r') as f:
            data = json.load(f)
        for cancion in data:
            cancion_obj = Cancion.objects.create(nombre=cancion['Cancion'], artista=cancion['Artista'], genero=cancion.get('Genero', ''), archivo=cancion['Archivo'])
            cancion_obj.save()
        return Response({'status': 'ok'}, status=status.HTTP_200_OK)