from django.contrib import admin
from .models import Pregunta, Tipo, Respuesta, Juego, Ronda

admin.site.register(Pregunta)
admin.site.register(Tipo)
admin.site.register(Respuesta)
admin.site.register(Juego)
admin.site.register(Ronda)