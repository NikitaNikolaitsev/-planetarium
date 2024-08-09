from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from planetarium.models import (
    ShowTheme,
    AstronomyShow,
    PlanetariumDome,
    Reservation,
    Ticket
)

User = get_user_model()


class AstronomyShowViewSetTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="example12313@.com",
            password="password"
        )
        self.client.force_authenticate(user=self.user)
        self.show_theme = ShowTheme.objects.create(name="Theme 1")
        self.astronomy_show = AstronomyShow.objects.create(
            title="Show",
            description="Description",
            show_theme=self.show_theme
        )
        self.astronomy_show_list_url = reverse(
            "planetarium:astronomy_show-list"
        )
        self.astronomy_show_detail_url = reverse(
            "planetarium:astronomy_show-detail", args=[self.astronomy_show.id]
        )

    def test_list_astronomy_shows(self):
        response = self.client.get(self.astronomy_show_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)

    def test_retrieve_astronomy_show(self):
        response = self.client.get(self.astronomy_show_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], self.astronomy_show.title)


class ShowThemeViewSetTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="example12313@.com",
            password="password"
        )
        self.client.force_authenticate(user=self.user)
        self.show_theme = ShowTheme.objects.create(name="Theme 1")
        self.show_theme_list_url = reverse("planetarium:showtheme-list")
        self.show_theme_detail_url = reverse(
            "planetarium:showtheme-detail", args=[self.show_theme.id]
        )

    def test_list_show_themes(self):
        response = self.client.get(self.show_theme_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)

    def test_retrieve_show_theme(self):
        response = self.client.get(self.show_theme_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], self.show_theme.name)


class PlanetariumDomeViewSetTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="example12313@.com",
            password="password"
        )
        self.client.force_authenticate(user=self.user)
        self.planetarium_dome = PlanetariumDome.objects.create(
            name="Dome 1", rows=10, seats_in_row=15
        )
        self.planetarium_dome_list_url = reverse("planetarium:planetariumdome-list")
        self.planetarium_dome_detail_url = reverse(
            "planetarium:planetariumdome-detail", args=[self.planetarium_dome.id]
        )

    def test_list_planetarium_domes(self):
        response = self.client.get(self.planetarium_dome_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)

    def test_retrieve_planetarium_dome(self):
        response = self.client.get(self.planetarium_dome_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], self.planetarium_dome.name)


class ReservationViewSetTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="example12313@.com",
            password="password"
        )
        self.client.force_authenticate(user=self.user)
        self.reservation = Reservation.objects.create(
            user=self.user, show_session=self.show_session
        )
        self.reservation_list_url = reverse("planetarium:reservation-list")
        self.reservation_detail_url = reverse(
            "planetarium:reservation-detail", args=[self.reservation.id]
        )

    def test_list_reservations(self):
        response = self.client.get(self.reservation_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)

    def test_retrieve_reservation(self):
        response = self.client.get(self.reservation_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data["user"], self.user.id
        )


class TicketViewSetTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="example12313@.com",
            password="password"
        )
        self.client.force_authenticate(user=self.user)
        self.ticket = Ticket.objects.create(
            reservation=self.reservation,
            seat_number=1,
            row_number=1,
        )
        self.ticket_list_url = reverse("planetarium:ticket-list")
        self.ticket_detail_url = reverse(
            "planetarium:ticket-detail", args=[self.ticket.id]
        )

    def test_list_tickets(self):
        response = self.client.get(self.ticket_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)

    def test_retrieve_ticket(self):
        response = self.client.get(self.ticket_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data["reservation"]["user"], self.user.id
        )
