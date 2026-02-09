from django.urls import path
from . import views
from api.views import (
    RegisterAPIView,
    LoginAPIView,
    UserUpdateAPIView,
    
    # DoctorDateAPIView,  # for pending dates
    appointments_list_create,
    approve_appointment,
    reject_appointment,
    delete_appointment,
)

from .views import create_render_admin


urlpatterns = [
    # --------------------
    # User APIs
    # --------------------
    path('register', RegisterAPIView.as_view(), name='register'),
    path('login', LoginAPIView.as_view(), name='login'),
    path('user/update/<int:pk>', UserUpdateAPIView.as_view(), name='user-update'),
    path("create-admin/", create_render_admin),

    # --------------------
    # Booking / Dates
    # --------------------
    # path("date/", DoctorDateAPIView.as_view(), name="pending-dates"),
    
    # --------------------
    # Appointment APIs
    # --------------------
    path('appointments/', views.appointments_list_create, name='appointments-list-create'),  # GET + POST
    path('appointments/<int:pk>/approve/', views.approve_appointment, name='appointments-approve'),
    path('appointments/<int:pk>/reject/', views.reject_appointment, name='appointments-reject'),
    path('appointments/<int:pk>/delete/', views.delete_appointment, name='appointments-delete'),
]
