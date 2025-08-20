from django.shortcuts import redirect
from django.contrib import messages
from django.views.generic import TemplateView
import pandas as pd
from django.conf import settings
from .models import Pregunta, Respuesta, Tipo, Juego, Ronda, Tipo
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import requests


############################### API CIEN MEXICANOS ############################################################################################

class NewQuestion(APIView):
    def get(self, request):
        tipo = Tipo.objects.get(tipo=request.GET.get('tipo'))
        pregunta = Pregunta.objects.filter(tipo=tipo).order_by('?').first()
        respuestas = Respuesta.objects.filter(pregunta=pregunta)
        juego = Juego.objects.all().order_by('-id').first()

        lista_respuestas = []
        for respuesta in respuestas:
            lista_respuestas.append({
                'id': respuesta.id,
                'respuesta': respuesta.respuesta,
                'calificacion': respuesta.calificacion,
            })

        ronda = Ronda.objects.create(
                    juego=juego,
                    pregunta=pregunta,
                    ronda=request.GET.get('ronda'),
                    errores=0,
                    robo=False,
                    turno='',
                    ganador='',
                    tipo=request.GET.get('puntos')
                )
        obj = {
            'id': ronda.id,
            'pregunta': ronda.pregunta.pregunta,
            'respuestas': lista_respuestas,
            'ronda': ronda.ronda,
            'errores': ronda.errores,
            'robo': ronda.robo,
            'turno': ronda.turno,
            'ganador': ronda.ganador,
            'terminada': ronda.terminada,
            'tipo': ronda.tipo,
        }

        requests.post(
            settings.WEBSOCKET_URL,
            json={"eventName": "ronda_"+ronda.ronda, "data": obj},
            timeout=10,
        )

        return Response(obj, status=status.HTTP_200_OK)

class StartGame(APIView):
    def post(self, request):
        data = request.data
        team1 = data.get('team1')
        team2 = data.get('team2')
        juego = Juego.objects.create(
                    team1=team1,
                    team2=team2,
                    team1_score=0,
                    team2_score=0,
                    game_started=True,
                    game_finished=False,
                    ganador=''
                )

        requests.post(
            settings.WEBSOCKET_URL,
            json={"eventName": "iniciar_juego", "data": {"team1": team1, "team2": team2, "juego": juego.id}},
            timeout=10,
        )
        return Response({'juego': juego.id}, status=status.HTTP_200_OK)

    def get(self, request):
        juego = Juego.objects.all().order_by('-id').first()

        obj = {
            "team1": juego.team1,
            "team2": juego.team2,
            "team1_score": juego.team1_score,
            "team2_score": juego.team2_score,
            "game_started": juego.game_started,
            "game_finished": juego.game_finished,
            "ganador": juego.ganador,
        }

        return Response(obj, status=status.HTTP_200_OK)

class RoundsView(APIView):
    def post(self, request):
        ronda = Ronda.objects.all().order_by('-id').first()
        respuestas = Respuesta.objects.filter(pregunta=ronda.pregunta)

        respuestas_list = []

        for respuesta in respuestas:
            respuestas_list.append({
                'id': respuesta.id,
                'respuesta': respuesta.respuesta,
                'calificacion': respuesta.calificacion,
            })

        obj = {
            'id': ronda.id,
            'pregunta': ronda.pregunta.pregunta,
            'respuestas': respuestas_list,
            'ronda': ronda.ronda,
            'errores': ronda.errores,
            'robo': ronda.robo,
            'turno': ronda.turno,
            'ganador': ronda.ganador,
            'terminada': ronda.terminada,
            'tipo': ronda.tipo,
        }

        return Response(obj, status=status.HTTP_200_OK)

class TurnoView(APIView):
    def post(self, request):
        data = request.data
        ronda = Ronda.objects.all().order_by('-id').first()
        if ronda.turno:
            ronda.robo = True
        ronda.turno = data.get('turno')
        ronda.save()

        obj = {
            'id': ronda.id,
            'robo': ronda.robo,
            'turno': ronda.turno,
            'ronda': ronda.ronda,
        }

        requests.post(
            settings.WEBSOCKET_URL,
            json={"eventName": "turno", "data": obj},
            timeout=10,
        )

        return Response(obj, status=status.HTTP_200_OK)

class CorrectAnswer(APIView):
    def post(self, request):
        data = request.data
        respuesta_correcta = Respuesta.objects.get(id=data.get('respuesta'))
        ronda = Ronda.objects.all().order_by('-id').first()

        obj = {
            'id': respuesta_correcta.id,
            'calificacion': respuesta_correcta.calificacion,
            'respuesta': respuesta_correcta.respuesta,
            'robo': ronda.robo,
            'terminada': ronda.terminada,
            'tipo': ronda.tipo,
        }

        requests.post(
            settings.WEBSOCKET_URL,
            json={"eventName": "respuesta_correcta", "data": obj},
            timeout=10,
        )

        return Response(obj, status=status.HTTP_200_OK)

class WrongAnswer(APIView):
    def post(self, request):
        ronda = Ronda.objects.all().order_by('-id').first()
        if ronda.turno and not ronda.robo:
            ronda.errores += 1
        ronda.save()

        if ronda.turno:
            obj = {
                'turno': True,
                'robo': ronda.robo,
                'terminada': ronda.terminada,
                'tipo': ronda.tipo,
            }
        else:

            obj = {
                'turno': False,
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

class FinishRound(APIView):
    def get(self, request):
        ronda = Ronda.objects.all().order_by('-id').first()
        ronda.ganador = ronda.turno
        ronda.save()

        obj = {
            'ganador': ronda.ganador,
            'ronda': ronda.ronda,
        }

        requests.post(
            settings.WEBSOCKET_URL,
            json={"eventName": "fin_ronda", "data": obj},
            timeout=10,
        )

        return Response(obj, status=status.HTTP_200_OK)

class RoundRobo(APIView):
    def post(self, request):
        data = request.data
        print(data)
        ronda = Ronda.objects.all().order_by('-id').first()
        juego = Juego.objects.all().order_by('-id').first()

        ronda.terminada = True
        ronda.save()

        if juego.team1 == ronda.turno:
            juego.team1_score += data.get('puntos')
            juego.save()
        else:
            juego.team2_score += data.get('puntos')
            juego.save()

        obj = {
            'terminada': ronda.terminada,
            'tipo': ronda.tipo,
        }

        requests.post(
            settings.WEBSOCKET_URL,
            json={"eventName": "robo", "data": obj},
            timeout=10,
        )

        return Response(obj, status=status.HTTP_200_OK)

class RoundNoRobo(APIView):
    def post(self, request):
        data = request.data
        ronda = Ronda.objects.all().order_by('-id').first()
        juego = Juego.objects.all().order_by('-id').first()

        if juego.team1 == ronda.turno:
            juego.team2_score += data.get('puntos')
            juego.save()
        else:
            juego.team1_score += data.get('puntos')
            juego.save()

        ronda.terminada = True
        if juego.team1 == ronda.turno:
            ronda.turno = juego.team2
        else:
            ronda.turno = juego.team1
        ronda.save()

        obj = {
            'terminada': ronda.terminada,
            'tipo': ronda.tipo,
        }

        requests.post(
            settings.WEBSOCKET_URL,
            json={"eventName": "no_robo", "data": obj},
            timeout=10,
        )

        return Response(obj, status=status.HTTP_200_OK)

class RoundGana(APIView):
    def post(self, request):
        data = request.data
        ronda = Ronda.objects.all().order_by('-id').first()
        juego = Juego.objects.all().order_by('-id').first()

        ronda.terminada = True
        ronda.save()

        if juego.team1 == ronda.turno:
            juego.team1_score += data.get('puntos')
            juego.save()
        else:
            juego.team2_score += data.get('puntos')
            juego.save()

        obj = {
            'terminada': ronda.terminada,
            'tipo': ronda.tipo,
        }

        requests.post(
            settings.WEBSOCKET_URL,
            json={"eventName": "gana", "data": obj},
            timeout=10,
        )

        return Response(obj, status=status.HTTP_200_OK)

class FinishGame(APIView):
    def get(self, request):
        juego = Juego.objects.all().order_by('-id').first()
        ronda = Ronda.objects.all().order_by('-id').first()
        juego.game_finished = True
        juego.ganador = juego.team1 if juego.team1_score > juego.team2_score else juego.team2
        juego.save()

        ronda.ganador = juego.ganador
        ronda.save()

        obj = {
            'game_finished': juego.game_finished,
            'ganador': juego.ganador,
        }

        requests.post(
            settings.WEBSOCKET_URL,
            json={"eventName": "fin_juego", "data": obj},
            timeout=10,
        )

        return Response(obj, status=status.HTTP_200_OK)

class ResetGame(APIView):
    def get(self, request):

        requests.post(
            settings.WEBSOCKET_URL,
            json={"eventName": "reset_game"},
            timeout=10,
        )

        return Response({'game_reset': True}, status=status.HTTP_200_OK)

class Upload100MxExcel(TemplateView):
    template_name = '100mx.html'

def upload_100mx(request):
    if request.method == 'POST':
        file = request.FILES.get('file')
        data = pd.read_excel(file)
        df = pd.DataFrame(data, columns=['tipo', 'pregunta', 'r1', 'r2', 'r3', 'r4', 'r5', 'c1', 'c2', 'c3', 'c4', 'c5'])
        for index, row in df.iterrows():
            tipo = Tipo.objects.filter(tipo=row['tipo']).first()
            if not tipo:
                Tipo.objects.create(tipo=row['tipo'])
        for index, row in df.iterrows():
            Pregunta.objects.create(tipo=Tipo.objects.get(tipo=row['tipo']), pregunta=row['pregunta'])
        for index, row in df.iterrows():
            pregunta = Pregunta.objects.get(pregunta=row['pregunta'])
            Respuesta.objects.create(pregunta=pregunta, respuesta=row['r1'], calificacion=row['c1'])
            Respuesta.objects.create(pregunta=pregunta, respuesta=row['r2'], calificacion=row['c2'])
            Respuesta.objects.create(pregunta=pregunta, respuesta=row['r3'], calificacion=row['c3'])
            Respuesta.objects.create(pregunta=pregunta, respuesta=row['r4'], calificacion=row['c4'])
            Respuesta.objects.create(pregunta=pregunta, respuesta=row['r5'], calificacion=row['c5'])

        messages.success(request, 'Preguntas cargadas correctamente')
        return redirect('cienmexicanos:cienmexicanos')

class KeyPressView(APIView):
    def post(self, request):
        data = request.data
        key = data.get('key')
        if key == 'enter':
            requests.post(
                settings.WEBSOCKET_URL,
                json={"eventName": "keypress", "data": {"key": "enter"}},
                timeout=10,
            )
        elif key == 'up':
            requests.post(
                settings.WEBSOCKET_URL,
                json={"eventName": "keypress", "data": {"key": "up"}},
                timeout=10,
            )
        elif key == 'down':
            requests.post(
                settings.WEBSOCKET_URL,
                json={"eventName": "keypress", "data": {"key": "down"}},
                timeout=10,
            )
        return Response({'status': 'ok'}, status=status.HTTP_200_OK)