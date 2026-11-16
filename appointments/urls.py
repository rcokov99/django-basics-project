from django.urls import path
from appointments.views import (
    appointment_list_view,
    appointment_create_view,
    appointment_edit_view,
    appointment_delete_view,
)

app_name = 'appointments'

urlpatterns = [
    path('', appointment_list_view, name='appointment-list'),
    path('add/', appointment_create_view, name='appointment-create'),
    path('<int:pk>/edit/', appointment_edit_view, name='appointment-edit'),
    path('<int:pk>/delete/', appointment_delete_view, name='appointment-delete'),
]