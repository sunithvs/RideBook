# RideShare API

A Django-based ride-sharing platform API that implements core functionalities similar to Uber. This project provides a robust backend system for managing ride bookings, user authentication, and real-time ride tracking.

## Features

### Core Features
- **User Management**
  - User registration and authentication
  - JWT-based authentication system
  - Separate driver and rider roles

- **Ride Management**
  - Create ride requests
  - View ride details
  - List all rides
  - Real-time status updates

- **Location Tracking**
  - Simulated real-time ride tracking
  - Current location updates
  - Trip history

- **Driver-Rider Matching**
  - Smart matching algorithm based on proximity
  - Driver ride acceptance system
  - Availability status management

### Technical Implementation
- Built with Django and Django Rest Framework
- Comprehensive API documentation
- Extensive test coverage
- Real-time updates using WebSocket

## Setup Instructions

1. Clone the repository:
```bash
git clone https://github.com/sunithvs/RideBook.git
cd rideshare
```

2. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run migrations:
```bash
python manage.py migrate
```

5. Start the development server:
```bash
python manage.py runserver
```

## API Endpoints

### Authentication
- `POST /api/auth/register/` - User registration
- `POST /api/auth/login/` - User login

### Rides
- `POST /api/rides/` - Create ride request
- `GET /api/rides/` - List all rides
- `GET /api/rides/<id>/` - Get ride details
- `PATCH /api/rides/<id>/` - Update ride status

### Driver
- `GET /api/rides/available/` - List available rides
- `POST /api/rides/<id>/accept/` - Accept ride request
- `PATCH /api/driver/status/` - Update availability status

## Testing

Run the test suite:
```bash
python manage.py test
```

## Tech Stack
- Django
- Django Rest Framework
- PostgreSQL
- Redis (for real-time features)
- pytest (for testing)

## License
This project is licensed under the MIT License - see the LICENSE.md file for details.
