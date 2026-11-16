from django.urls import path
from specialists.views import (
    doctor_list_view,
    doctor_detail_view,
    department_list_view,
    department_create_view,
)

app_name = 'specialists'

urlpatterns = [
    # Doctors
    path('doctors/', doctor_list_view, name='doctor-list'),
    path('doctors/<int:pk>/', doctor_detail_view, name='doctor-detail'),

    # Departments
    path('departments/', department_list_view, name='department-list'),
    path('departments/add/', department_create_view, name='department-create'),
]