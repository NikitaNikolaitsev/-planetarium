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
router.register(r'showthemes', ShowThemeViewSet)
router.register(r'astronomyshows', AstronomyShowViewSet)
router.register(r'planetariumdomes', PlanetariumDomeViewSet)
router.register(r'showsessions', ShowSessionViewSet)
router.register(r'reservations', ReservationViewSet)
router.register(r'tickets', TicketViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
