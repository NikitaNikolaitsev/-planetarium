from datetime import datetime
from django.db.models import F, Count
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

from planetarium.models import (
    ShowTheme,
    AstronomyShow,
    PlanetariumDome,
    ShowSession,
    Reservation,
    Ticket,
)
from planetarium.permissions import IsAdminOrIfAuthenticatedReadOnly
from planetarium.serializers import (
    ShowThemeSerializer,
    AstronomyShowSerializer,
    PlanetariumDomeSerializer,
    ShowSessionSerializer,
    ReservationSerializer,
    TicketSerializer,
    AstronomyShowRetrieveSerializer,
    TicketRetrieveSerializer,
    ShowSessionTicketSerializer
)


class ShowThemeViewSet(viewsets.ModelViewSet):
    queryset = ShowTheme.objects.all()
    serializer_class = ShowThemeSerializer
    permission_classes = [IsAdminOrIfAuthenticatedReadOnly]


class AstronomyShowViewSet(viewsets.ModelViewSet):
    queryset = AstronomyShow.objects.all()
    serializer_class = AstronomyShowSerializer
    permission_classes = [IsAdminOrIfAuthenticatedReadOnly]

    def get_queryset(self):
        queryset = AstronomyShow.objects.all()
        title = self.request.query_params.get("title")
        theme = self.request.query_params.get("theme")

        if title:
            queryset = queryset.filter(title__icontains=title)
        if theme:
            queryset = queryset.filter(show_theme__name__icontains=theme)
        return queryset.distinct()

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return AstronomyShowRetrieveSerializer
        return self.serializer_class


class PlanetariumDomeViewSet(viewsets.ModelViewSet):
    queryset = PlanetariumDome.objects.all()
    serializer_class = PlanetariumDomeSerializer
    permission_classes = [IsAdminOrIfAuthenticatedReadOnly]

    def get_queryset(self):
        queryset = PlanetariumDome.objects.all()
        name = self.request.query_params.get("name")

        if name:
            queryset = queryset.filter(name__icontains=name)

        return queryset.distinct()


class ShowSessionViewSet(viewsets.ModelViewSet):
    queryset = ShowSession.objects.select_related(
        "astronomy_show",
        "planetarium_dome",
    ).annotate(
        tickets_available=(F("planetarium_dome__rows") * F("planetarium_dome__seats_in_row") - Count("tickets"))
    )
    serializer_class = ShowSessionSerializer

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ShowSessionTicketSerializer
        return self.serializer_class

    @action(
        methods=["GET"],
        detail=False,
        permission_classes=[IsAuthenticated],
    )
    def nearest_show(self, request):
        now = datetime.now()
        nearest_session = self.get_queryset().filter(show_time__gte=now).order_by("show_time").first()

        if nearest_session:
            serializer = self.get_serializer(nearest_session)
            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)


class ReservationViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Reservation.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class TicketViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        queryset = Ticket.objects.filter(reservation__user=user).select_related(
            "show__astronomy_show",
            "show__planetarium_dome",
            "reservation",
        )

        show_title = self.request.query_params.get("show_title")
        if show_title:
            queryset = queryset.filter(show__astronomy_show__title__icontains=show_title)

        return queryset.distinct()

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return TicketRetrieveSerializer
        return self.serializer_class
