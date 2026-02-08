<!-- Appointment Booking API -->

This project is an Appointment Booking Web Application built using Django Rest Framework. It provides APIs for users, appointments, authentication, and integrates with a WordPress frontend form.

<!-- Getting Started  -->

Follow these steps to run the project on your local machine:

<!-- Technologies -->

Python

Django

Django Rest Framework

SQLite (default) — PostgreSQL optional

Html, CSS, JavaScript(Admin Dashboard)

WordPress (frontend integration)

<!-- ---------------------- Installation -------------------- -->

<!-- Clone the repository: -->

git clone https://github.com/majidovnurbek/Appointment_Booking_API.git
cd Appointment_Booking_API


<!-- Create a virtual environment (optional): -->

python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows


<!-- Install the required dependencies: -->

pip install -r requirements.txt


<!-- Apply database migrations: -->

python manage.py migrate


<!-- Create a superuser (optional): -->

python manage.py createsuperuser


<!-- Start the development server: -->

python manage.py runserver


<!-- Access the API: -->

API root: http://127.0.0.1:8000/api/

Admin dashboard: http://127.0.0.1:8000/admin/

Swagger docs: http://127.0.0.1:8000/api/schema/swagger-ui/

Redoc docs: http://127.0.0.1:8000/api/schema/redoc/

<!-- Notes -->

Default database is SQLite (db.sqlite3).

WordPress frontend form can submit appointments to /api/appointments/.

JWT authentication is enabled for protected routes.