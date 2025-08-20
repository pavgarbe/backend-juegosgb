from django.urls import path
from .views import *
from django.conf import settings

app_name = 'juegosfuerza'

urlpatterns = [
    path("ajustar-creditos/", AjustarCreditosAPIView.as_view(), name="ajustar-creditos"),
    path("historial-ajustes/", HistorialAjustesAPIView.as_view(), name="historial-ajustes"),
    path("historial-monedas/", HistorialMonedasAPIView.as_view(), name="historial-monedas"),
    path("creditos/", ObtenerCreditosAPIView.as_view(), name="obtener-creditos"),
    path("creditos/gastar/", GastarCreditosAPIView.as_view(), name="gastar-creditos"),
    # path("inicio/", EntrarInicioAPIView.as_view(), name="inicio"),
    # path("entrar-menu/", EntrarMenuAPIView.as_view(), name="entrar-menu"),
    # path("iniciar-juego/", IniciarJuegoAPIView.as_view(), name="iniciar-juego"),
    # path("nivel-juego/", NivelJuegoAPIView.as_view(), name="nivel-juego"),
    path("iniciar-toques/", IniciarToquesAPIView.as_view(), name="iniciar-toques"),
    path("fin-juego/", FinJuegoAPIView.as_view(), name="fin-juego"),
    path("pera/", PeraAPIView.as_view(), name="pera"),
    path("fuerza/", FuerzaAPIView.as_view(), name="fuerza"),
]