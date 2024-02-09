#  Internship Task Django

## Introduction

Welcome to the project README! This document provides an overview of the various modules and components present in your Django project.

## auth_login

The `auth_login` app handles user authentication, registration, and user profile management.

### Modules

- **models.py**: Defines custom user models with additional fields like mobile number, profile image, and more.

- **views.py**: Contains views for user authentication, profile management, login via Google OAuth2, email and password login, user registration, and more.

- **serializers.py**: Provides serializers for user data, login credentials, and registration data.

- **urls.py**: Defines URLs for user authentication, login, registration, profile management, and more.

## base

The `base` app includes base models, utility classes, and custom permissions.

### Modules

- **models.py**: Contains an abstract base model with timestamp fields, active status, and soft delete functionality.

- **permissions.py**: Defines custom permissions like `IsOwner`, `IsVerified`, `IsNotVerified`, and `IsOwnObj` for controlling access based on ownership and verification status.

## Installation

To get started with the project, follow these steps:

1. Clone the repository to your local machine.
2. Set up a virtual environment for the project
   - On Windows: `python -m venv venv`
   - On macOS and Linux: `python3 -m venv venv`
4. Activate the virtual environment:
   - On Windows: `venv\Scripts\activate`
   - On macOS and Linux: `source venv/bin/activate`
5. Install project dependencies using `pip install -r requirements.txt`.
6. Run makemigrations using `python manage.py makemigrations`.
7. Run migrations using `python manage.py migrate`.
8. Create a superuser account using `python manage.py createsuperuser`.

## Usage

- The `auth_login` app provides user authentication, login, registration, and profile management views.
- Use the custom permissions defined in the `base` app to control access to various API endpoints.
- Customize the models, serializers, and views to fit your project's requirements.

## Running with Docker

You can also run the project using Docker for easy setup and management. Follow these steps:

1. Make sure you have Docker installed on your system.
2. Clone the repository to your local machine.
3. Open a terminal and navigate to the project directory.
4. copy the `.env.example` file to `.env` and fill in the required values.
5. Build the Docker image: `docker compose build .`
6. Run the Docker container: `docker compose up `
7. Access the project at `http://localhost:8000/`.

Remember to replace `project-name` with your actual project's name.

