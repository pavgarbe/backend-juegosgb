from django.db import models



class Genero(models.Model):
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre


class Artista(models.Model):
    nombre = models.CharField(max_length=100)
    genero = models.ForeignKey(Genero, on_delete=models.CASCADE, related_name='artistas', null=True, blank=True)

    def __str__(self):
        return self.nombre


class Cancion(models.Model):
    nombre = models.CharField(max_length=100)
    artista = models.ForeignKey(Artista, on_delete=models.CASCADE)
    audio = models.FileField(upload_to='canciones/audio/', blank=True, null=True)

    def __str__(self):
        return f"{self.nombre} - {self.artista.nombre}"

class Juego(models.Model):
    team1 = models.CharField(max_length=50)
    team2 = models.CharField(max_length=50)
    team1_score = models.IntegerField(default=0)
    team2_score = models.IntegerField(default=0)
    game_started = models.BooleanField(default=False)
    game_finished = models.BooleanField(default=False)
    ganador = models.CharField(max_length=50, blank=True, null=True)
    rondas = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.team1} vs {self.team2}"

class Ronda(models.Model):
    juego = models.ForeignKey(Juego, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=50, choices=[('Sencilla', 'Sencilla'), ('Doble', 'Doble'), ('Triple', 'Triple')])
    ronda = models.IntegerField(default=0)
    terminada = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.juego} - Ronda {self.ronda}"

class CancionEquipo(models.Model):
    cancion = models.ForeignKey(Cancion, on_delete=models.CASCADE)
    ronda = models.ForeignKey(Ronda, on_delete=models.CASCADE)
    equipo = models.CharField(max_length=100)
    robo = models.BooleanField(default=False)
    equipo_robo = models.CharField(max_length=100, blank=True, null=True)
    terminada = models.BooleanField(default=False)
    ganador = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.equipo} - {self.cancion} - {self.ronda}"

