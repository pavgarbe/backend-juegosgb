from django.db import models

class Tipo(models.Model):
    tipo = models.CharField(max_length=50)

    def __str__(self):
        return self.tipo

class Pregunta(models.Model):
    tipo = models.ForeignKey(Tipo, on_delete=models.CASCADE)
    pregunta = models.TextField()

    def __str__(self):
        return self.pregunta

class Respuesta(models.Model):
    pregunta = models.ForeignKey(Pregunta, on_delete=models.CASCADE)
    respuesta = models.TextField()
    calificacion = models.IntegerField()

    def __str__(self):
        return self.respuesta

class Juego(models.Model):
    team1 = models.CharField(max_length=50)
    team2 = models.CharField(max_length=50)
    team1_score = models.IntegerField(default=0)
    team2_score = models.IntegerField(default=0)
    game_started = models.BooleanField(default=False)
    game_finished = models.BooleanField(default=False)
    ganador = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return f"{self.team1} vs {self.team2}"

class Ronda(models.Model):
    tipo = models.CharField(max_length=50, default="Sencilla")
    juego = models.ForeignKey(Juego, on_delete=models.CASCADE)
    pregunta = models.ForeignKey(Pregunta, on_delete=models.CASCADE)
    ronda = models.IntegerField()
    errores = models.IntegerField(default=0)
    robo = models.BooleanField(default=False)
    turno = models.CharField(max_length=50)
    terminada = models.BooleanField(default=False)
    ganador = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return f"{self.juego} - {self.pregunta} - Ronda {self.ronda}"

