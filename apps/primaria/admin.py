from django.contrib import admin
from .models import Pregunta, Respuesta, Juego, Ronda, PreguntaEquipo

admin.site.register(Pregunta)
admin.site.register(Respuesta)
admin.site.register(Juego)
admin.site.register(Ronda)
admin.site.register(PreguntaEquipo)