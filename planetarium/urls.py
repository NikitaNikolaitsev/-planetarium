from django.urls import path, include
from rest_framework.routers import DefaultRouter

from planetarium.views import (
    TicketViewSet,
    ReservationViewSet,
    ShowSessionViewSet,
    PlanetariumDomeViewSet,
    AstronomyShowViewSet,
    ShowThemeViewSet
)

app_name = 'planetarium'

router = DefaultRouter()
router.register("show_themes", ShowThemeViewSet, basename='show_theme')
router.register("astronomy_shows", AstronomyShowViewSet, basename='astronomy_show')
router.register("planetarium_domes", PlanetariumDomeViewSet, basename='planetarium_dome')
router.register("reservations", ReservationViewSet)
router.register("tickets", TicketViewSet, basename='ticket')

urlpatterns = [
    path('', include(router.urls)),
]
