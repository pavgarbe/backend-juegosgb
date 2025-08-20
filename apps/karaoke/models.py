from django.db import models

class Cancion(models.Model):
    nombre = models.CharField(max_length=100)
    artista = models.CharField(max_length=100)
    genero = models.CharField(max_length=50, blank=True, null=True)
    archivo = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.nombre} - {self.artista} ({self.genero})" if self.genero else f"{self.nombre} - {self.artista}"

    class Meta:
        verbose_name = "Canción"
        verbose_name_plural = "Canciones"
        ordering = ['nombre']

