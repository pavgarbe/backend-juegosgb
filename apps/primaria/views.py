from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import requests
from .models import Pregunta, Respuesta, Juego, Ronda, PreguntaEquipo
from django.views.generic import TemplateView
import pandas as pd
from django.shortcuts import redirect
from django.contrib import messages
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
        preguntas_ronda = data.get('rondaPreguntas')
        juego = Juego.objects.create(team1=team1, team2=team2, team1_score=0, team2_score=0, game_started=True, game_finished=False, ganador='', preguntas_ronda=preguntas_ronda)

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
            "preguntas_ronda": juego.preguntas_ronda,
        }

        return Response(obj, status=status.HTTP_200_OK)

class RoundsView(APIView):
    def post(self, request):
        data = request.data
        juego = Juego.objects.all().order_by('-id').first()
        ronda = Ronda.objects.create(juego=juego, ronda=data.get('ronda'), terminada=False, tipo=data.get('tipo'))

        requests.post(
            settings.WEBSOCKET_URL,
            json={"eventName": "ronda_"+str(ronda.ronda), "data": {"ronda": ronda.ronda, "tipo": ronda.tipo , "id": ronda.id}},
            timeout=10,
        )

        return Response({'ronda': ronda.id}, status=status.HTTP_200_OK)

    def get(self, request):
        ronda = Ronda.objects.all().order_by('-id').first()
        preguntas = PreguntaEquipo.objects.filter(ronda=ronda).count()
        obj = {
            'id': ronda.id,
            'ronda': ronda.ronda,
            'terminada': ronda.terminada,
            'tipo': ronda.tipo,
            'preguntas': preguntas,
        }

        return Response(obj, status=status.HTTP_200_OK)


class QuestionView(APIView):
    def post(self, request):
        data = request.data
        ronda = Ronda.objects.all().order_by('-id').first()
        juego = Juego.objects.all().order_by('-id').first()

        pregunta = None

        if data.get('ronda') == 1:
            pregunta = Pregunta.objects.filter(grado='1ero', materia=data.get('materia'), tipo=data.get('tipo')).order_by('?').first()
        elif data.get('ronda') == 2:
            pregunta = Pregunta.objects.filter(grado='2do', materia=data.get('materia'), tipo=data.get('tipo')).order_by('?').first()
        elif data.get('ronda') == 3:
            pregunta = Pregunta.objects.filter(grado='3ero', materia=data.get('materia'), tipo=data.get('tipo')).order_by('?').first()
        elif data.get('ronda') == 4:
            pregunta = Pregunta.objects.filter(grado='4to', materia=data.get('materia'), tipo=data.get('tipo')).order_by('?').first()
        elif data.get('ronda') == 5:
            pregunta = Pregunta.objects.filter(grado='5to', materia=data.get('materia'), tipo=data.get('tipo')).order_by('?').first()
        elif data.get('ronda') == 6:
            pregunta = Pregunta.objects.filter(grado='6to', materia=data.get('materia'), tipo=data.get('tipo')).order_by('?').first()

        preguntas_equipo = PreguntaEquipo.objects.filter(ronda=ronda).first()
        if preguntas_equipo is not None:
            if preguntas_equipo.pregunta == pregunta:
                pregunta_equipo = PreguntaEquipo.objects.create(ronda=ronda, pregunta=Pregunta.objects.filter(grado=pregunta.grado, materia=pregunta.materia, tipo=pregunta.tipo).order_by('?').first(), equipo=juego.team2)
            else:
                pregunta_equipo = PreguntaEquipo.objects.create(ronda=ronda, pregunta=pregunta, equipo=juego.team2)
        else:
            pregunta_equipo = PreguntaEquipo.objects.create(ronda=ronda, pregunta=pregunta, equipo=juego.team1)

        respuestas = Respuesta.objects.filter(pregunta=pregunta).order_by('respuesta')
        respuestas_list = []
        for respuesta in respuestas:
            respuestas_list.append({
                'id': respuesta.id,
                'respuesta': respuesta.respuesta,
                'correcta': respuesta.correcta,
            })

        obj = {
            'id': pregunta_equipo.id,
            'pregunta': pregunta_equipo.pregunta.pregunta,
            'respuestas': respuestas_list,
            'equipo': pregunta_equipo.equipo,
            'ronda': ronda.ronda,
            'tipo': ronda.tipo,
            'materia': pregunta.materia,
            'grado': pregunta.grado,
            'robo': pregunta_equipo.robo,
            'equipo_robo': pregunta_equipo.equipo_robo,
            'terminada': pregunta_equipo.terminada,
            'ganador': pregunta_equipo.ganador,
        }

        requests.post(
            settings.WEBSOCKET_URL,
            json={"eventName": "pregunta", "data": obj},
            timeout=10,
        )

        return Response(obj, status=status.HTTP_200_OK)

    def get(self, request):
        ronda = Ronda.objects.all().order_by('-id').first()
        pregunta_equipo = PreguntaEquipo.objects.filter(ronda=ronda).order_by('-id').first()

        respuestas = Respuesta.objects.filter(pregunta=pregunta_equipo.pregunta).order_by('respuesta')
        respuestas_list = []
        for respuesta in respuestas:
            respuestas_list.append({
                'id': respuesta.id,
                'respuesta': respuesta.respuesta,
                'correcta': respuesta.correcta,
            })

        obj = {
            'id': pregunta_equipo.id,
            'pregunta': pregunta_equipo.pregunta.pregunta,
            'respuestas': respuestas_list,
            'equipo': pregunta_equipo.equipo,
            'ronda': ronda.ronda,
            'tipo': pregunta_equipo.pregunta.tipo,
            'grado': pregunta_equipo.pregunta.grado,
            'materia': pregunta_equipo.pregunta.materia,
            'robo': pregunta_equipo.robo,
            'equipo_robo': pregunta_equipo.equipo_robo,
            'terminada': pregunta_equipo.terminada,
            'ganador': pregunta_equipo.ganador,
        }

        return Response(obj, status=status.HTTP_200_OK)



class CorrectAnswer(APIView):
    def get(self, request):
        ronda = Ronda.objects.all().order_by('-id').first()
        pregunta_equipo = PreguntaEquipo.objects.filter(ronda=ronda).order_by('-id').first()
        juego = Juego.objects.all().order_by('-id').first()
        preguntas = PreguntaEquipo.objects.filter(ronda=ronda).count()
        ganador = None

        if pregunta_equipo.robo:
            if pregunta_equipo.equipo == juego.team1:
                if ronda.tipo == 'Sencilla':
                    juego.team2_score += 1
                elif ronda.tipo == 'Doble':
                    juego.team2_score += 2
                elif ronda.tipo == 'Triple':
                    juego.team2_score += 3
                ganador = juego.team2
                pregunta_equipo.ganador = juego.team2
            else:
                if ronda.tipo == 'Sencilla':
                    juego.team1_score += 1
                elif ronda.tipo == 'Doble':
                    juego.team1_score += 2
                elif ronda.tipo == 'Triple':
                    juego.team1_score += 3
                ganador = juego.team1
                pregunta_equipo.ganador = juego.team1
        else:
            if pregunta_equipo.equipo == juego.team1:
                if ronda.tipo == 'Sencilla':
                    juego.team1_score += 1
                elif ronda.tipo == 'Doble':
                    juego.team1_score += 2
                elif ronda.tipo == 'Triple':
                    juego.team1_score += 3
                ganador = juego.team1
                pregunta_equipo.ganador = juego.team1
            else:
                if ronda.tipo == 'Sencilla':
                    juego.team2_score += 1
                elif ronda.tipo == 'Doble':
                    juego.team2_score += 2
                elif ronda.tipo == 'Triple':
                    juego.team2_score += 3
                ganador = juego.team2
                pregunta_equipo.ganador = juego.team2

        if ronda.ronda == 6 and juego.preguntas_ronda == preguntas:
            if juego.team1_score > juego.team2_score:
                juego.ganador = juego.team1
            elif juego.team2_score > juego.team1_score:
                juego.ganador = juego.team2
            else:
                juego.ganador = 'Empate'

        juego.save()

        pregunta_equipo.terminada = True
        pregunta_equipo.save()

        if preguntas == juego.preguntas_ronda:
            ronda.terminada = True
            ronda.save()

        obj = {
            'team1_score': juego.team1_score,
            'team2_score': juego.team2_score,
            'ganador': ganador,
            'terminada': ronda.terminada,
            'p_terminada': pregunta_equipo.terminada,
            'tipo': ronda.tipo,
            'respuesta': request.GET.get('respuesta'),
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
        pregunta_equipo = PreguntaEquipo.objects.filter(ronda=ronda).order_by('-id').first()
        juego = Juego.objects.all().order_by('-id').first()
        preguntas = PreguntaEquipo.objects.filter(ronda=ronda).count()

        if not pregunta_equipo.robo:
            pregunta_equipo.robo = True
            if pregunta_equipo.equipo == juego.team1:
                pregunta_equipo.equipo_robo = juego.team2
            else:
                pregunta_equipo.equipo_robo = juego.team1
        else:
            pregunta_equipo.terminada = True

            if preguntas == juego.preguntas_ronda:
                ronda.terminada = True
                ronda.save()

            requests.post(
                settings.WEBSOCKET_URL,
                json={"eventName": "no-winner", "data": {"terminada": ronda.terminada}},
                timeout=10,
            )

        pregunta_equipo.save()

        obj = {
            'robo': pregunta_equipo.robo,
            'respuesta': request.GET.get('respuesta'),
            'p_terminada': pregunta_equipo.terminada,
            'terminada': ronda.terminada,
            'tipo': ronda.tipo,
        }

        requests.post(
            settings.WEBSOCKET_URL,
            json={"eventName": "respuesta_incorrecta", "data": obj},
            timeout=10,
        )

        return Response(obj, status=status.HTTP_200_OK)


class EndQuestion(APIView):
    def get(self, request):
        ronda = Ronda.objects.all().order_by('-id').first()
        pregunta_equipo = PreguntaEquipo.objects.filter(ronda=ronda).order_by('-id').first()

        pregunta_equipo.terminada = True
        pregunta_equipo.save()

        obj = {
            'terminada': pregunta_equipo.terminada,
            'robo': pregunta_equipo.robo,
            'equipo_robo': pregunta_equipo.equipo_robo,
        }

        requests.post(
            settings.WEBSOCKET_URL,
            json={"eventName": "fin_pregunta", "data": obj},
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

        ronda.terminada = True
        ronda.save()

        obj = {
            'terminada': ronda.terminada,
        }

        requests.post(
            settings.WEBSOCKET_URL,
            json={"eventName": "fin_ronda", "data": obj},
            timeout=10,
        )

        return Response(obj, status=status.HTTP_200_OK)

class FinishGame(APIView):
    def get(self, request):
        juego = Juego.objects.all().order_by('-id').first()
        juego.game_finished = True
        juego.ganador = juego.team1 if juego.team1_score > juego.team2_score else juego.team2
        juego.save()

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

class UploadPrimariaExcel(TemplateView):
    template_name = 'primaria.html'

def upload_primaria(request):
    if request.method == 'POST':
        file = request.FILES.get('file')
        data = pd.read_excel(file)
        df = pd.DataFrame(data, columns=['numero', 'tipo', 'grado', 'materia', 'pregunta', 'o1', 'o2', 'o3', 'o4', 'o5'])
        for index, row in df.iterrows():
            pregunta = Pregunta.objects.create(tipo=row['tipo'], grado=row['grado'], materia=row['materia'], pregunta=row['pregunta'])
            Respuesta.objects.create(pregunta=pregunta, respuesta=row['o1'], correcta=True)
            if row['numero'] == 4:
                Respuesta.objects.create(pregunta=pregunta, respuesta=row['o2'], correcta=False)
                Respuesta.objects.create(pregunta=pregunta, respuesta=row['o3'], correcta=False)
                Respuesta.objects.create(pregunta=pregunta, respuesta=row['o4'], correcta=False)
            if row['numero'] == 5:
                Respuesta.objects.create(pregunta=pregunta, respuesta=row['o2'], correcta=False)
                Respuesta.objects.create(pregunta=pregunta, respuesta=row['o3'], correcta=False)
                Respuesta.objects.create(pregunta=pregunta, respuesta=row['o4'], correcta=False)
                Respuesta.objects.create(pregunta=pregunta, respuesta=row['o5'], correcta=False)

        messages.success(request, 'Preguntas cargadas correctamente')
        return redirect('primaria:primaria')
