from django.contrib import admin
from .models import User, Date, Appointment

# -----------------------
# Date Admin
# -----------------------
@admin.register(Date)
class DateAdmin(admin.ModelAdmin):
    list_display = ('user', 'date', 'time', 'status')
    search_fields = ('status',)

# -----------------------
# User Admin
# -----------------------
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_staff', 'is_active')
    search_fields = ('username', 'email')

# -----------------------
# Appointment Admin
# -----------------------
@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'service', 'date', 'status', 'created_at')
    search_fields = ('name', 'email', 'service')
    list_filter = ('status',)
