from django.db import models

juegos = (
    ("Boxeo", "Boxeo"),
    ("Martillo", "Martillo"),
    ("Vencidas", "Vencidas"),
    ("Toques", "Toques")
)


class Juego(models.Model):
    juego = models.CharField(max_length=50, choices=juegos, default="Boxeo")
    creado = models.DateTimeField(auto_now_add=True)
    monto = models.IntegerField(default=0)

    def __str__(self):
        return self.juego + " - " + str(self.creado)

class ImagenJuego(models.Model):
    juego = models.ForeignKey(Juego, on_delete=models.CASCADE)
    imagen = models.ImageField(upload_to='juegos/')
    creado = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.juego.juego + " - " + str(self.creado)


class Creditos(models.Model):
    total = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.id}"


class MonedaInsertada(models.Model):
    fecha = models.DateField(auto_now_add=True)
    hora = models.TimeField(auto_now_add=True)
    moneda = models.IntegerField(null=True, blank=True)  # Valor detectado
    pulsos = models.IntegerField()  # Pulsos reales

    def __str__(self):
        return f"{self.fecha} {self.hora} - 💰 {self.moneda} pesos ({self.pulsos} pulsos)"


class ReinicioCreditos(models.Model):
    fecha = models.DateTimeField(auto_now_add=True)
    hora = models.TimeField(auto_now_add=True)
    valor_anterior = models.IntegerField()
    nuevo_valor = models.IntegerField()
    motivo = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.fecha} - Valor anterior: {self.valor_anterior}, seteado a: {self.nuevo_valor}"
