from django.urls import path
from .views import *
from django.conf import settings
# === importar vistas de juegosfuerza para reusar endpoints ===
from apps.juegosfuerza.views import (
    AjustarCreditosAPIView,
    HistorialAjustesAPIView,
    HistorialMonedasAPIView,
    ObtenerCreditosAPIView,
)

app_name = 'cienmexicanos'

urlpatterns = [
    path('new-question/', NewQuestion.as_view(), name='new_question'),
    path('start-game/', StartGame.as_view(), name='start_game'),
    path('finish-game/', FinishGame.as_view(), name='finish_game'),
    path('reset-game/', ResetGame.as_view(), name='reset_game'),
    path('round/', RoundsView.as_view(), name='ronda'),
    path('turno/', TurnoView.as_view(), name='turno'),
    path('correct-answer/', CorrectAnswer.as_view(), name='answer'),
    path('timer/', TimerView.as_view(), name='timer'),
    path('wrong-answer/', WrongAnswer.as_view(), name='wrong_answer'),
    path('round/robo/', RoundRobo.as_view(), name='robo'),
    path('round/no-robo/', RoundNoRobo.as_view(), name='robo'),
    path('round/finish/', FinishRound.as_view(), name='finish_round'),
    path('round/gana/', RoundGana.as_view(), name='gana'),
    path('', Upload100MxExcel.as_view(), name='cienmexicanos'),
    path('upload/', upload_100mx, name='upload'),
    path('key-press/', KeyPressView.as_view(), name='key_press'),
    path('ajustar-creditos/', AjustarCreditosAPIView.as_view(), name='ajustar-creditos'),
    path('historial-ajustes/', HistorialAjustesAPIView.as_view(), name='historial-ajustes'),
    path('historial-monedas/', HistorialMonedasAPIView.as_view(), name='historial-monedas'),
    path('creditos/', ObtenerCreditosAPIView.as_view(), name='creditos'),
]