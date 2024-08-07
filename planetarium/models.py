from django.db import models
from django.conf import settings


class ShowTheme(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()

    def __str__(self):
        return self.title


class AstronomyShow(models.Model):
    title = models.CharField(max_length=200)
    themes = models.ManyToManyField(ShowTheme, related_name='astronomy_shows')
    description = models.TextField()


class PlanetariumDome(models.Model):
    name = models.CharField(max_length=200)
    rows = models.IntegerField()
    seats_in_row = models.IntegerField()


class ShowSession(models.Model):
    astronomy_show = models.ForeignKey(AstronomyShow, on_delete=models.CASCADE, related_name='sessions')
    planetarium_dome = models.ForeignKey(PlanetariumDome, on_delete=models.CASCADE, related_name='sessions')
    show_time = models.DateTimeField()

    def __str__(self):
        return f"{self.astronomy_show.title} - {self.show_time}"


class Reservation(models.Model):
    id = models.AutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reservations')


class Ticket(models.Model):
    row = models.IntegerField()
    seats = models.IntegerField()
    show = models.ForeignKey(ShowSession, on_delete=models.CASCADE, related_name='tickets')
    reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE, related_name='tickets')
