from django.db import models

GRADOS = (
    ("1ero", "1ero"),
    ("2do", "2do"),
    ("3ero", "3ero"),
    ("4to", "4to"),
    ("5to", "5to"),
    ("6to", "6to")
)

TIPOS = (
    ("Abierta", "Abierta"),
    ("Opciones", "Opciones")
)

MATERIAS = (
    ("Matematicas", "Matematicas"),
    ("Español", "Español"),
    ("Ciencias Naturales", "Ciencias Naturales"),
    ("Ciencias Sociales", "Ciencias Sociales"),
    ("Geografia", "Geografia"),
    ("Historia", "Historia"),
    ("Artes", "Artes")
)

class Pregunta(models.Model):
    tipo = models.CharField(max_length=50, choices=TIPOS, default="Abierta")
    grado = models.CharField(max_length=50, choices=GRADOS, default="1ero")
    materia = models.CharField(max_length=50, choices=MATERIAS, default="Matematicas")
    pregunta = models.TextField()

    def __str__(self):
        return self.pregunta

class Respuesta(models.Model):
    pregunta = models.ForeignKey(Pregunta, on_delete=models.CASCADE)
    respuesta = models.TextField()
    correcta = models.BooleanField(default=False)

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
    preguntas_ronda = models.IntegerField(default=2)

    def __str__(self):
        return f"{self.team1} vs {self.team2}"

class Ronda(models.Model):
    juego = models.ForeignKey(Juego, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=50, default="Sencilla")
    ronda = models.IntegerField(default=0)
    terminada = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.juego} - Ronda {self.ronda}"

class PreguntaEquipo(models.Model):
    ronda = models.ForeignKey(Ronda, on_delete=models.CASCADE)
    pregunta = models.ForeignKey(Pregunta, on_delete=models.CASCADE)
    equipo = models.CharField(max_length=100)
    robo = models.BooleanField(default=False)
    equipo_robo = models.CharField(max_length=100, blank=True, null=True)
    terminada = models.BooleanField(default=False)
    ganador = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.equipo} - {self.pregunta} - {self.ronda}"

