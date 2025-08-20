from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import os
import json
import requests
from .models import Juego, Ronda, Cancion, CancionEquipo, Artista, Genero
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import requests
from django.conf import settings

class StartGame(APIView):
    def post(self, request):
        data = request.data
        team1 = data.get('team1')
        team2 = data.get('team2')
        juego = Juego.objects.create(team1=team1, team2=team2, team1_score=0, team2_score=0, game_started=True, game_finished=False, ganador='', rondas=data.get('rondas'))

        requests.post(
            settings.WEBSOCKET_URL,
            json={"eventName": "iniciar_juego", "data": {"id": juego.id}},
            timeout=10,
        )
        return Response({'id': juego.id}, status=status.HTTP_200_OK)

    def get(self, request):
        juego = Juego.objects.all().order_by('-id').first()

        obj = {
            "id": juego.id,
            "team1": juego.team1,
            "team2": juego.team2,
            "team1_score": juego.team1_score,
            "team2_score": juego.team2_score,
            "game_started": juego.game_started,
            "game_finished": juego.game_finished,
            "ganador": juego.ganador,
            "rondas": juego.rondas,
        }

        return Response(obj, status=status.HTTP_200_OK)

class RoundsView(APIView):
    def post(self, request):
        data = request.data
        juego = Juego.objects.all().order_by('-id').first()
        ronda = Ronda.objects.create(juego=juego, ronda=data.get('ronda'), terminada=False, tipo=data.get('tipo'))

        requests.post(
            settings.WEBSOCKET_URL,
            json={"eventName": "ronda", "data": {"ronda": ronda.ronda, "tipo": ronda.tipo , "id": ronda.id}},
            timeout=10,
        )

        return Response({'ronda': ronda.id}, status=status.HTTP_200_OK)

    def get(self, request):
        ronda = Ronda.objects.all().order_by('-id').first()
        canciones = CancionEquipo.objects.filter(ronda=ronda).count()
        obj = {
            'id': ronda.id,
            'ronda': ronda.ronda,
            'terminada': ronda.terminada,
            'tipo': ronda.tipo,
            'canciones': canciones,
        }

        return Response(obj, status=status.HTTP_200_OK)


class QuestionView(APIView):
    def post(self, request):
        data = request.data
        ronda = Ronda.objects.all().order_by('-id').first()
        juego = Juego.objects.all().order_by('-id').first()
        genero = data.get('genero') if data.get('genero') else None
        artista = data.get('artista') if data.get('artista') else None

        cancion = None

        if genero and not artista:
            cancion = Cancion.objects.filter(artista__genero=Genero.objects.filter(nombre=genero).first()).order_by('?').first()
        elif genero and artista:
            cancion = Cancion.objects.filter(artista=Artista.objects.filter(nombre=artista).first(), artista__genero=Genero.objects.filter(nombre=genero).first()).order_by('?').first()
        else:
            cancion = Cancion.objects.all().order_by('?').first()

        canciones_equipo = CancionEquipo.objects.filter(ronda=ronda).first()

        if canciones_equipo is not None:
            if canciones_equipo.cancion == cancion:
                cancion_equipo = CancionEquipo.objects.create(ronda=ronda, cancion=Cancion.objects.all().order_by('?').first(), equipo=juego.team2)
            else:
                cancion_equipo = CancionEquipo.objects.create(ronda=ronda, cancion=cancion, equipo=juego.team2)
        else:
            cancion_equipo = CancionEquipo.objects.create(ronda=ronda, cancion=cancion, equipo=juego.team1)

        obj = {
            'id': cancion_equipo.id,
            'cancion': cancion_equipo.cancion.nombre,
            'artista': cancion_equipo.cancion.artista.nombre,
            'genero': cancion_equipo.cancion.artista.genero.nombre,
            'audio': request.build_absolute_uri(cancion_equipo.cancion.audio.url),
            'equipo': cancion_equipo.equipo,
            'ronda': ronda.ronda,
            'tipo': ronda.tipo,
            'robo': cancion_equipo.robo,
            'equipo_robo': cancion_equipo.equipo_robo,
            'terminada': cancion_equipo.terminada,
            'ganador': cancion_equipo.ganador,
        }

        requests.post(
            settings.WEBSOCKET_URL,
            json={"eventName": "pregunta", "data": obj},
            timeout=10,
        )

        return Response(obj, status=status.HTTP_200_OK)

    def get(self, request):
        ronda = Ronda.objects.all().order_by('-id').first()
        cancion_equipo = CancionEquipo.objects.filter(ronda=ronda).order_by('-id').first()

        obj = {
            'id': cancion_equipo.id,
            'cancion': cancion_equipo.cancion.nombre,
            'artista': cancion_equipo.cancion.artista.nombre,
            'genero': cancion_equipo.cancion.artista.genero.nombre,
            'audio': request.build_absolute_uri(cancion_equipo.cancion.audio.url),
            'equipo': cancion_equipo.equipo,
            'ronda': ronda.ronda,
            'robo': cancion_equipo.robo,
            'equipo_robo': cancion_equipo.equipo_robo,
            'terminada': cancion_equipo.terminada,
            'ganador': cancion_equipo.ganador,
        }

        return Response(obj, status=status.HTTP_200_OK)



class CorrectAnswer(APIView):
    def get(self, request):
        ronda = Ronda.objects.all().order_by('-id').first()
        cancion_equipo = CancionEquipo.objects.filter(ronda=ronda).order_by('-id').first()
        juego = Juego.objects.all().order_by('-id').first()
        canciones = CancionEquipo.objects.filter(ronda=ronda).count()
        ganador = None

        if cancion_equipo.robo:
            if cancion_equipo.equipo == juego.team1:
                if ronda.tipo == 'Sencilla':
                    juego.team2_score += 1
                elif ronda.tipo == 'Doble':
                    juego.team2_score += 2
                elif ronda.tipo == 'Triple':
                    juego.team2_score += 3
                ganador = juego.team2
                cancion_equipo.ganador = juego.team2
            else:
                if ronda.tipo == 'Sencilla':
                    juego.team1_score += 1
                elif ronda.tipo == 'Doble':
                    juego.team1_score += 2
                elif ronda.tipo == 'Triple':
                    juego.team1_score += 3
                ganador = juego.team1
                cancion_equipo.ganador = juego.team1

        else:
            if cancion_equipo.equipo == juego.team1:
                if ronda.tipo == 'Sencilla':
                    juego.team1_score += 1
                elif ronda.tipo == 'Doble':
                    juego.team1_score += 2
                elif ronda.tipo == 'Triple':
                    juego.team1_score += 3
                ganador = juego.team1
                cancion_equipo.ganador = juego.team1
            else:
                if ronda.tipo == 'Sencilla':
                    juego.team2_score += 1
                elif ronda.tipo == 'Doble':
                    juego.team2_score += 2
                elif ronda.tipo == 'Triple':
                    juego.team2_score += 3
                ganador = juego.team2
                cancion_equipo.ganador = juego.team2

        if ronda.ronda == juego.rondas and canciones == 2:
            if juego.team1_score > juego.team2_score:
                juego.ganador = juego.team1
            elif juego.team2_score > juego.team1_score:
                juego.ganador = juego.team2
            else:
                juego.ganador = 'Empate'

        juego.save()

        cancion_equipo.terminada = True
        cancion_equipo.save()

        if canciones == 2:
            ronda.terminada = True
            ronda.save()

        obj = {
            'team1_score': juego.team1_score,
            'team2_score': juego.team2_score,
            'ganador': ganador,
            'terminada': ronda.terminada,
            'p_terminada': cancion_equipo.terminada,
            'tipo': ronda.tipo,
            'cancion': cancion_equipo.cancion.nombre,
            'artista': cancion_equipo.cancion.artista.nombre,
            'genero': cancion_equipo.cancion.artista.genero.nombre,
        }

        requests.post(
            settings.WEBSOCKET_URL,
            json={"eventName": "respuesta_correcta", "data": obj},
            timeout=10,
        )

        return Response(obj, status=status.HTTP_200_OK)

class WrongAnswer(APIView):
    def get(self, request):
        ronda = Ronda.objects.all().order_by('-id').first()
        cancion_equipo = CancionEquipo.objects.filter(ronda=ronda).order_by('-id').first()
        juego = Juego.objects.all().order_by('-id').first()
        canciones = CancionEquipo.objects.filter(ronda=ronda).count()

        if not cancion_equipo.robo:
            cancion_equipo.robo = True
            if cancion_equipo.equipo == juego.team1:
                cancion_equipo.equipo_robo = juego.team2
            else:
                cancion_equipo.equipo_robo = juego.team1
        else:
            cancion_equipo.terminada = True

            if canciones == 2:
                ronda.terminada = True
                ronda.save()

        if ronda.ronda == juego.rondas and canciones == 2:
            if juego.team1_score > juego.team2_score:
                juego.ganador = juego.team1
            elif juego.team2_score > juego.team1_score:
                juego.ganador = juego.team2
            else:
                juego.ganador = 'Empate'

        juego.save()

        cancion_equipo.save()

        obj = {
            'robo': cancion_equipo.robo,
            'p_terminada': cancion_equipo.terminada,
            'terminada': ronda.terminada,
            'tipo': ronda.tipo,
            'cancion': cancion_equipo.cancion.nombre,
            'artista': cancion_equipo.cancion.artista.nombre,
            'genero': cancion_equipo.cancion.artista.genero.nombre,
        }

        requests.post(
            settings.WEBSOCKET_URL,
            json={"eventName": "respuesta_incorrecta", "data": obj},
            timeout=10,
        )

        return Response(obj, status=status.HTTP_200_OK)


class TimerView(APIView):
    def get(self, request):
        start = True if request.GET.get('start') == 'true' else False

        print(request.GET.get('start'))

        if start:
            print('iniciar')
            requests.post(
                settings.WEBSOCKET_URL,
                json={"eventName": "inicio_cronometro", "data": {"start": start}},
                timeout=10,
            )
        if not start:
            print('parar')
            requests.post(
                settings.WEBSOCKET_URL,
                json={"eventName": "fin_cronometro", "data": {"start": start}},
                timeout=10,
            )

        return Response({'start': start}, status=status.HTTP_200_OK)

class ResetGame(APIView):
    def get(self, request):

        requests.post(
            settings.WEBSOCKET_URL,
            json={"eventName": "reset_game"},
            timeout=10,
        )

        return Response({'game_reset': True}, status=status.HTTP_200_OK)

class GetArtistas(APIView):
    def get(self, request):
        artistas = Artista.objects.filter(genero__nombre=request.GET.get('genero'))
        data = [{"id": artista.id, "nombre": artista.nombre} for artista in artistas]

        return Response(data, status=status.HTTP_200_OK)

class GetGeneros(APIView):
    def get(self, request):
        generos = Genero.objects.all()
        data = [{"id": genero.id, "nombre": genero.nombre} for genero in generos]

        return Response(data, status=status.HTTP_200_OK)

class UploadCanciones(APIView):
    def get(self, request):
        file = os.path.join(settings.BASE_DIR, 'apps/adivinacancion/base_canciones.json')
        with open(file, 'r') as f:
            data = json.load(f)
        for cancion in data:
            genero, created = Genero.objects.get_or_create(nombre=cancion['Genero'])
            artista, created = Artista.objects.get_or_create(nombre=cancion['NombreArtista'], genero=genero)
            cancion_obj = Cancion.objects.create(nombre=cancion['NombreCancion'], artista=artista, audio='canciones/audio/'+cancion['NombreArchivo'])
            cancion_obj.save()
        return Response({'status': 'ok'}, status=status.HTTP_200_OK)


class PlayAudio(APIView):
    def get(self, request):
        cancion = CancionEquipo.objects.filter(ronda__terminada=False).order_by('-id').first()

        requests.post(
            settings.WEBSOCKET_URL,
            json={"eventName": "play_audio", "data": {'audio': request.build_absolute_uri(cancion.cancion.audio.url), 'id': cancion.id}},
            timeout=10,
        )

        return Response({'audio': request.build_absolute_uri(cancion.cancion.audio.url)}, status=status.HTTP_200_OK)

