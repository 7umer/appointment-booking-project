
# Appointment Booking Project (Django + Admin Dashboard + WordPress)

This project is an Appointment Booking Web Application built using Django Rest Framework.
It provides APIs for appointment booking, JWT authentication, and includes a separate
HTML/CSS/JS Admin Dashboard. A WordPress frontend form is used for user booking.

---

## Technologies Used

- Python
- Django
- Django Rest Framework
- SQLite (default database)
- HTML, CSS, JavaScript (Admin Dashboard)
- WordPress (Frontend booking form)
- JWT Authentication

---

## Project Structure

- Admin_Dashboard/ → Frontend admin panel (HTML/JS/CSS)
- Appointment_Booking_API/ → Django backend
- WordPress form → Hosted separately (Elementor)

---

## Installation (Backend)

## Clone your repository:

git clone https://github.com/7umer/appointment-booking-project.git
cd appointment-booking-project/Appointment_Booking_API


## Create virtual environment:

python -m venv venv
venv\Scripts\activate


## Install dependencies:

pip install -r requirements.txt


## Run migrations:

python manage.py migrate


## Create admin user:

python manage.py createsuperuser



## Start server:

python manage.py runserver


## Access URLs

API Root:
http://127.0.0.1:8000/api/

Admin Panel:
http://127.0.0.1:8000/admin/

Swagger Docs:
http://127.0.0.1:8000/api/schema/swagger-ui/

Redoc Docs:
http://127.0.0.1:8000/api/schema/redoc/

---

## Notes

- Default database: SQLite (db.sqlite3)
- Admin Dashboard uses API endpoints from Django
- WordPress form sends appointments to:

   /api/appointments/

- JWT authentication protects admin actions

## Author

Umer