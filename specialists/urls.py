from django.urls import path
from specialists.views import (
    department_create_view,
    department_list_view,
    doctor_detail_view,
    doctor_list_view,
    service_create_view,
    service_list_view,
)

app_name = 'specialists'

urlpatterns = [
    # Doctors
    path('doctors/', doctor_list_view, name='doctor-list'),
    path('doctors/<int:pk>/', doctor_detail_view, name='doctor-detail'),

    # Departments
    path('departments/', department_list_view, name='department-list'),
    path('departments/add/', department_create_view, name='department-create'),

    # Services
    path('services/', service_list_view, name='service-list'),
    path('services/add/', service_create_view, name='service-create'),
]