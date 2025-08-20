from django.contrib import admin
from .models import Juego, Ronda, Cancion, CancionEquipo, Artista, Genero

admin.site.register(Juego)
admin.site.register(Ronda)
admin.site.register(Cancion)
admin.site.register(CancionEquipo)
admin.site.register(Artista)
admin.site.register(Genero)