from django.urls import path
from .views import *

app_name = 'primaria'

urlpatterns = [
    path('start-game/', StartGame.as_view(), name='start_game'),
    path('finish-game/', FinishGame.as_view(), name='finish_game'),
    path('reset-game/', ResetGame.as_view(), name='reset_game'),
    path('round/', RoundsView.as_view(), name='ronda'),
    path('round/finish/', FinishRound.as_view(), name='finish_round'),
    path('question/', QuestionView.as_view(), name='question'),
    path('correct-answer/', CorrectAnswer.as_view(), name='answer'),
    path('wrong-answer/', WrongAnswer.as_view(), name='wrong_answer'),
    path('end-question/', EndQuestion.as_view(), name='end_question'),
    path('timer/', TimerView.as_view(), name='timer'),
    path('', UploadPrimariaExcel.as_view(), name='primaria'),
    path('upload/', upload_primaria, name='upload'),

]