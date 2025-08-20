from django.urls import path
from .views import *

app_name = 'adivinacancion'

urlpatterns = [
    path('start-game/', StartGame.as_view(), name='start_game'),
    path('reset-game/', ResetGame.as_view(), name='reset_game'),
    path('round/', RoundsView.as_view(), name='ronda'),
    path('question/', QuestionView.as_view(), name='question'),
    path('correct-answer/', CorrectAnswer.as_view(), name='answer'),
    path('wrong-answer/', WrongAnswer.as_view(), name='wrong_answer'),
    path('timer/', TimerView.as_view(), name='timer'),
    path('generos/', GetGeneros.as_view(), name='generos'),
    path('artistas/', GetArtistas.as_view(), name='artistas'),
    path('upload/', UploadCanciones.as_view(), name='upload_audio'),
    path('play-audio/', PlayAudio.as_view(), name='play_audio'),
]