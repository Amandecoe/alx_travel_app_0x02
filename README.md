# Travel App

A Django-based travel booking application with integrated payment via Chapa. Users can create listings, make bookings, and pay for their bookings. The project also supports email notifications using Celery.

## Features

### Listings

Create, view, and manage travel listings.

Each listing is owned by a registered user.

### Bookings

Users can book listings.

Bookings track start and end dates, total price, and status (pending/confirmed/admin).

### Payments

Integrated with Chapa
 for online payments.

Users can initiate and verify payments.

Payment status is tracked in the database.

### Email Notifications

Confirmation emails sent on successful bookings and payments.

Handled asynchronously using Celery.

## API

Fully RESTful API built with Django REST Framework (DRF).

Swagger documentation available for API endpoints.

## Project Setup
### Prerequisites

* Python 3.10+

* Django 4.x

* Django REST Framework

* MySQL (via XAMPP or MariaDB)

* Chapa Sandbox Account (for payment testing)

## Clone the repository
git clone <repository-url>
cd alx_travel_app

## Install dependencies
pip install -r requirements.txt

## Environment Variables

Create a .env file in the project root:

SECRET_KEY=<your-django-secret-key>
DEBUG=True
DB_NAME=<your-database-name>
DB_USER=<your-database-user>
DB_PASSWORD=<your-database-password>
DB_HOST=localhost
DB_PORT=3306
CHAPA_SECRET_KEY=<your-chapa-secret-key>


Use python-decouple or django-environ to load .env in settings.py.

## Database Setup

Make sure your MySQL/XAMPP server is running.

python manage.py makemigrations
python manage.py migrate


## Create a superuser:

python manage.py createsuperuser

##API Endpoints
### Authentication

Obtain JWT Token

POST /api/token/
{
  "username": "<your-username>",
  "password": "<your-password>"
}


Returns access and refresh tokens.

Use token in headers for protected endpoints:

Authorization: Bearer <access-token>

## Listings

Create a listing: POST /api/listings/

List all listings: GET /api/listings/

Retrieve a listing: GET /api/listings/<id>/

Update a listing: PUT /api/listings/<id>/

Delete a listing: DELETE /api/listings/<id>/

Example POST body:

{
  "title": "Awesome Hotel",
  "description": "A cozy place to stay",
  "price": 2000
}

## Bookings

Create a booking: POST /api/bookings/

List bookings: GET /api/bookings/

Retrieve a booking: GET /api/bookings/<id>/

Example POST body:

{
  "listing": 1,
  "start_date": "2025-09-15T12:00:00Z",
  "end_date": "2025-09-20T12:00:00Z",
  "total_price": 10000
}

## Payments

Initiate payment: POST /api/payments/initiate/

{
  "booking_id": 1,
  "amount": 10000
}


Verify payment: POST /api/payments/verify/

{
  "tx_ref": "<transaction-reference>"
}

Swagger Documentation

Available at:

GET /swagger/

## Celery Setup

### Install Celery:

pip install celery


Configure Celery in settings.py:

CELERY_BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'


Run Celery worker:

celery -A alx_travel_app worker -l info

## Testing

Use Postman or any REST client to test endpoints.

Chapa Sandbox URLs are used for payment testing:

Payment initiation: https://api.chapa.co/v1/transaction/initialize

Payment verification: https://api.chapa.co/v1/transaction/verify/{tx_ref}

# Notes

Listings must exist before bookings — bookings require a listing_id.

Bookings must exist before initiating payment — payments require a valid booking_id.

Use JWT tokens in all POST/PUT/DELETE requests for authenticated users.
