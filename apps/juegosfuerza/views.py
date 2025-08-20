from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from datetime import datetime, timedelta
import threading
import time
import requests
import serial
from django.conf import settings
from .models import Creditos, MonedaInsertada, ReinicioCreditos, Juego, ImagenJuego

arduino = serial.Serial(port=settings.ARDUINO_PORT, baudrate=9600, timeout=.1)

def escuchar_arduino():
    while True:
        try:
            while arduino.in_waiting > 0:
                try:
                    raw = arduino.readline()
                    try:
                        mensaje = raw.decode('utf-8', errors='replace').strip()
                    except Exception as e:
                        print(f"Error decodificando: {e}, raw: {raw}")
                        continue
                    print(f"[DEBUG] Mensaje recibido crudo: {repr(mensaje)}")
                    if not mensaje:
                        continue
                    if mensaje == "#SALDO01#":
                        creditos = Creditos.objects.get(id=1)
                        creditos.total += 1
                        creditos.save()
                        moneda_insertada = MonedaInsertada.objects.create(
                            fecha=timezone.now().date(),
                            hora=timezone.now().time(),
                            moneda=1,
                            pulsos=1
                        )
                        requests.post(
                            settings.WEBSOCKET_URL,
                            json={"eventName": "creditos", "data": 1},
                            timeout=10,
                        )
                        print(f"Saldo actualizado: {creditos.total} créditos")
                    elif mensaje == "#SALDO02#":
                        creditos = Creditos.objects.get(id=1)
                        creditos.total += 2
                        creditos.save()
                        moneda_insertada = MonedaInsertada.objects.create(
                            fecha=timezone.now().date(),
                            hora=timezone.now().time(),
                            moneda=2,
                            pulsos=1
                        )
                        requests.post(
                            settings.WEBSOCKET_URL,
                            json={"eventName": "creditos", "data": 2},
                            timeout=10,
                        )
                        print(f"Saldo actualizado: {creditos.total} créditos")
                    elif mensaje == "#SALDO05#":
                        creditos = Creditos.objects.get(id=1)
                        creditos.total += 5
                        creditos.save()
                        moneda_insertada = MonedaInsertada.objects.create(
                            fecha=timezone.now().date(),
                            hora=timezone.now().time(),
                            moneda=5,
                            pulsos=1
                        )
                        requests.post(
                            settings.WEBSOCKET_URL,
                            json={"eventName": "creditos", "data": 5},
                            timeout=10,
                        )
                        print(f"Saldo actualizado: {creditos.total} créditos")
                    elif mensaje == "#SALDO10#":
                        creditos = Creditos.objects.get(id=1)
                        creditos.total += 10
                        creditos.save()
                        moneda_insertada = MonedaInsertada.objects.create(
                            fecha=timezone.now().date(),
                            hora=timezone.now().time(),
                            moneda=10,
                            pulsos=1
                        )
                        requests.post(
                            settings.WEBSOCKET_URL,
                            json={"eventName": "creditos", "data": 10},
                            timeout=10,
                        )
                        print(f"Saldo actualizado: {creditos.total} créditos")
                    elif mensaje == "#SALDO20#":
                        creditos = Creditos.objects.get(id=1)
                        creditos.total += 20
                        creditos.save()
                        moneda_insertada = MonedaInsertada.objects.create(
                            fecha=timezone.now().date(),
                            hora=timezone.now().time(),
                            moneda=20,
                            pulsos=1
                        )
                        requests.post(
                            settings.WEBSOCKET_URL,
                            json={"eventName": "creditos", "data": 20},
                            timeout=10,
                        )
                        print(f"Saldo actualizado: {creditos.total} créditos")
                    elif mensaje == "#SALDO00#":
                        moneda_insertada = MonedaInsertada.objects.create(
                            fecha=timezone.now().date(),
                            hora=timezone.now().time(),
                            moneda=0,
                            pulsos=1
                        )
                        print("Moneda no reconocida")
                    elif mensaje == "#BOTON00#":
                        requests.post(
                            settings.WEBSOCKET_URL,
                            json={"eventName": "keypress", "data": {"key": "right"}},
                            timeout=10,
                        )
                        print("Botón Arriba")
                    elif mensaje == "#BOTON01#":
                        requests.post(
                            settings.WEBSOCKET_URL,
                            json={"eventName": "keypress", "data": {"key": "left"}},
                            timeout=10,
                        )
                        print("Botón Abajo")
                    elif mensaje == "#BOTON02#":
                        requests.post(
                            settings.WEBSOCKET_URL,
                            json={"eventName": "keypress", "data": {"key": "enter"}},
                            timeout=10,
                        )
                        print("Botón Enter")
                    elif mensaje == "#BOTON03#":
                        requests.post(
                            settings.WEBSOCKET_URL,
                            json={"eventName": "keypress", "data": {"key": "return"}},
                            timeout=10,
                        )
                        print("Botón Regresar")
                    elif mensaje == "#LISTOJUEGO#":
                         requests.post(
                            settings.WEBSOCKET_URL,
                            json={"eventName": "listo", "data": 1},
                            timeout=10,
                        )
                         print("Listo Juego")
                    elif mensaje == "#FINJUEGO#":
                         requests.post(
                            settings.WEBSOCKET_URL,
                            json={"eventName": "fin", "data": 1},
                            timeout=10,
                        )
                         print("Fin Juego")
                    elif mensaje.startswith("#FUERZA"):
                        fuerza = mensaje.split("FUERZA")[1].split("#")[0]
                        fuerza = int(fuerza)
                        print(f"Fuerza detectada: {fuerza}")
                        requests.post(
                            settings.WEBSOCKET_URL,
                            json={"eventName": "fuerza", "data": fuerza},
                            timeout=10,
                        )
                    elif mensaje == "#GANANDO01#":
                        requests.post(
                            settings.WEBSOCKET_URL,
                            json={"eventName": "ganando-maquina", "data": 1},
                            timeout=10,
                        )
                        print("Ganando Maquina")
                    elif mensaje == "#GANANDO02#":
                        requests.post(
                            settings.WEBSOCKET_URL,
                            json={"eventName": "ganando-jugador", "data": 1},
                            timeout=10,
                        )
                        print("Ganando Jugador")
                    elif mensaje == "#GANO01#":
                        requests.post(
                            settings.WEBSOCKET_URL,
                            json={"eventName": "gano-maquina", "data": 1},
                            timeout=10,
                        )
                        print("Ganó Maquina")
                    elif mensaje == "#GANO02#":
                        requests.post(
                            settings.WEBSOCKET_URL,
                            json={"eventName": "gano-jugador", "data": 1},
                            timeout=10,
                        )
                        print("Ganó Jugador")
                    elif mensaje == "#PERA-ABAJO#":
                        requests.post(
                            settings.WEBSOCKET_URL,
                            json={"eventName": "pera", "data": 1},
                            timeout=10,
                        )
                        print("Pera detectada")
                    elif mensaje == "#INICIOTOQUES#":
                        requests.post(
                            settings.WEBSOCKET_URL,
                            json={"eventName": "inicio", "data": 1},
                            timeout=10,
                        )
                        print("Iniciando juego de toques")
                    elif mensaje == "#FINJUEGO#":
                        requests.post(
                            settings.WEBSOCKET_URL,
                            json={"eventName": "fin", "data": 1},
                            timeout=10,
                        )
                        print("Fin del juego")
                    else:
                        print(f"Mensaje no reconocido: {mensaje}")
                except Exception as e:
                    print(f"Error al procesar mensaje: {e}")
            time.sleep(0.05)
        except Exception as e:
            print(f"Error al leer de Arduino: {e}")
            time.sleep(0.1)

hilo_arduino = threading.Thread(target=escuchar_arduino, daemon=True)
hilo_arduino.start()

class EntrarInicioAPIView(APIView):
    def get(self, request):
        arduino.write('35')
        time.sleep(0.05)

        return Response({'1'}, status=status.HTTP_200_OK)

class AjustarCreditosAPIView(APIView):
        def post(self, request):
            data = request.data
            nueva_cantidad = data.get("nuevo_valor")
            password = data.get("password")

            if password != settings.CREDITOS_PASSWORD:
                return Response({"error": "Contraseña incorrecta"}, status=status.HTTP_403_FORBIDDEN)

            creditos = Creditos.objects.get(id=1)
            valor_anterior = creditos.total
            creditos.total = nueva_cantidad
            creditos.save()

            ReinicioCreditos.objects.create(
                valor_anterior=valor_anterior,
                valor_seteado=nueva_cantidad,
                motivo=data.get("motivo", "")
            )

            return Response({"mensaje": "Créditos actualizados correctamente", "nuevo_total": creditos.total}, status=status.HTTP_200_OK)



class HistorialAjustesAPIView(APIView):
        def get(self, request):
            tipo = request.query_params.get("tipo", "dia")

            hoy = datetime.now()
            if tipo == "ayer":
                desde = hoy - timedelta(days=1)
                hasta = hoy.replace(hour=0, minute=0, second=0, microsecond=0)
            elif tipo == "semana":
                desde = hoy - timedelta(days=7)
                hasta = hoy
            elif tipo == "mes":
                desde = hoy - timedelta(days=30)
                hasta = hoy
            else:
                desde = hoy.replace(hour=0, minute=0, second=0, microsecond=0)
                hasta = hoy

            ajustes = ReinicioCreditos.objects.filter(fecha__gte=desde, fecha__lte=hasta).order_by("-fecha")

            data = [
                {
                    "fecha": r.fecha.strftime("%Y-%m-%d %H:%M:%S"),
                    "valor_anterior": r.valor_anterior,
                    "nuevo_valor": r.nuevo_valor,
                    "motivo": r.motivo
                }
                for r in ajustes
            ]
            return Response(data)


class ObtenerCreditosAPIView(APIView):
        def get(self, request):
            creditos = Creditos.objects.get(id=1)
            return Response({"total": creditos.total})


class GastarCreditosAPIView(APIView):
        def post(self, request):
            data = request.data
            cantidad = data.get("cantidad")
            juego = data.get("juego")

            creditos = Creditos.objects.get(id=1)
            if creditos.total >= cantidad:
                creditos.total -= cantidad
                creditos.save()

                game = Juego.objects.create(juego=juego, monto=cantidad)

                return Response({"juego": game.id, "monto": cantidad}, status=status.HTTP_200_OK)
            else:
                return Response({"error": "No hay suficientes créditos"}, status=status.HTTP_400_BAD_REQUEST)


class HistorialMonedasAPIView(APIView):
        def get(self, request):
            tipo = request.query_params.get("tipo", "dia")
            hoy = datetime.now()

            if tipo == "ayer":
                desde = hoy - timedelta(days=1)
                hasta = hoy.replace(hour=0, minute=0, second=0, microsecond=0)
            elif tipo == "semana":
                desde = hoy - timedelta(days=7)
                hasta = hoy
            elif tipo == "mes":
                desde = hoy - timedelta(days=30)
                hasta = hoy
            else:
                desde = hoy.replace(hour=0, minute=0, second=0, microsecond=0)
                hasta = hoy

            registros = MonedaInsertada.objects.filter(fecha__gte=desde.date(), fecha__lte=hasta.date()).order_by("-fecha", "-hora")

            resumen = registros.values("moneda").order_by("moneda")

            data = {
                "resumen": list(resumen),
                "registros": [
                    {
                        "fecha": r.fecha.strftime("%Y-%m-%d"),
                        "hora": r.hora.strftime("%H:%M:%S") if r.hora else "",
                        "moneda": r.moneda,
                        "pulsos": r.pulsos
                    }
                    for r in registros
                ]
            }

            return Response(data)

class EntrarMenuAPIView(APIView):
    def get(self, request):
        menu = request.GET.get('menu')
        if menu == 'inicio':
            arduino.write(bytes('#MENU00#', 'utf-8'))
            print('#MENU00#')
        elif menu == 'toques':
            arduino.write(bytes('#MENU01#', 'utf-8'))
            print('#MENU01#')
        elif menu == 'boxeo':
            arduino.write(bytes('#MENU02#', 'utf-8'))
            print('#MENU02#')
        elif menu == 'vencidas':
            arduino.write(bytes('#MENU03#', 'utf-8'))
            print('#MENU03#')
        elif menu == 'martillo':
            arduino.write(bytes('#MENU04#', 'utf-8'))
            print('#MENU04#')
        else:
            return Response({'error': 'Menu no válido'}, status=status.HTTP_400_BAD_REQUEST)
        time.sleep(0.05)

        return Response(menu, status=status.HTTP_200_OK)

class IniciarJuegoAPIView(APIView):
    def get(self, request):
        juego = request.GET.get('juego')
        credito = request.GET.get('creditos')
        print ('credito introducido', credito)
        creditos = Creditos.objects.get(id=1)
        creditos.total -= int(credito)
        creditos.save()
        print ('credito restante', creditos.total)
        if juego == 'toques':
            arduino.write(bytes('START_TOQUES\n', 'utf-8'))
            print('START_TOQUES\n')
        elif juego == 'boxeo':
            arduino.write(bytes('START_BOX\n', 'utf-8'))
            print('START_BOX\n')
        elif juego == 'vencidas':
            arduino.write(bytes('START_VENCIDAS\n', 'utf-8'))
            print('START_VENCIDAS\n')
        elif juego == 'martillo':
            arduino.write(bytes('START_MARTILLO\n', 'utf-8'))
            print('START_MARTILLO\n')
        else:
            return Response({'error': 'Juego no válido'}, status=status.HTTP_400_BAD_REQUEST)
        time.sleep(0.05)
        return Response({'mensaje': 'Juego iniciado'}, status=status.HTTP_200_OK)


class NivelJuegoAPIView(APIView):
    def get(self, request):
        nivel = request.GET.get('nivel')
        arduino.write(bytes(f'#NIVEL{nivel}#', 'utf-8'))
        time.sleep(0.05)
        return Response({'mensaje': f'Nivel {nivel} seteado'}, status=status.HTTP_200_OK)

class IniciarToquesAPIView(APIView):
    def get(self, request):
        requests.post(
            settings.WEBSOCKET_URL,
            json={"eventName": "inicio", "data": 1},
            timeout=10,
        )

        return Response({'mensaje': 'Juego de toques iniciado'}, status=status.HTTP_200_OK)

class FinJuegoAPIView(APIView):
    def get(self, request):
        requests.post(
            settings.WEBSOCKET_URL,
            json={"eventName": "fin", "data": 1},
            timeout=10,
        )

        return Response({'mensaje': 'Juego finalizado'}, status=status.HTTP_200_OK)

class PeraAPIView(APIView):
    def get(self, request):
        requests.post(
            settings.WEBSOCKET_URL,
            json={"eventName": "pera", "data": 1},
            timeout=10,
        )

        return Response({'mensaje': 'Pera detectada'}, status=status.HTTP_200_OK)

class FuerzaAPIView(APIView):
    def get(self, request):
        fuerza = 500
        requests.post(
            settings.WEBSOCKET_URL,
            json={"eventName": "fuerza", "data": fuerza},
            timeout=10,
        )

        return Response({'mensaje': f'Fuerza {fuerza} detectada'}, status=status.HTTP_200_OK)