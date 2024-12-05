# Planetarium Service

This is a web application built using Django REST Framework (DRF) for managing a planetarium. The project provides functionality for managing shows, booking reservations, and ticketing.

## Features

- **Show Management**: Create and manage astronomy shows with various themes.
- **Dome Management**: Manage planetarium domes where shows are displayed.
- **Session Scheduling**: Schedule show sessions and manage bookings.
- **Reservation System**: Allow users to book seats for specific shows.
- **Ticketing**: Issue and manage tickets for reserved seats.

## Models

The application includes the following key models:

- `ShowTheme`: Represents different themes for astronomy shows.
- `AstronomyShow`: Contains details about each show, including title, description, and duration.
- `PlanetariumDome`: Represents the domes where shows are presented.
- `ShowSession`: Schedules for shows, including start time and available seats.
- `Reservation`: Manages user reservations for specific sessions.
- `Ticket`: Represents tickets issued to users for specific reservations.

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/planetarium-service.git
   cd planetarium-service
pip install -r requirements.txt

use 
   python manage.py loaddata load_planetarium.jso

![screenshots](/static/readme1.png)
![screenshots](/static/readme2.png)
![screenshots](/static/readme3.png)
![screenshots](/static/readme4.png)
![screenshots](/static/readme5.png)
