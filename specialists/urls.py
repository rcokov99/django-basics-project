from django.urls import path
from specialists.views import (
    department_create_view,
    department_list_view,
    doctor_create_view,
    doctor_delete_view,
    doctor_detail_view,
    doctor_edit_view,
    doctor_list_view,
    service_create_view,
    service_list_view,
    service_detail_view,
)

app_name = 'specialists'

urlpatterns = [
    path('doctors/', doctor_list_view, name='doctor-list'),
    path('doctors/add/', doctor_create_view, name='doctor-create'),
    path('doctors/<int:pk>/', doctor_detail_view, name='doctor-detail'),
    path('doctors/<int:pk>/edit/', doctor_edit_view, name='doctor-edit'),
    path('doctors/<int:pk>/delete/', doctor_delete_view, name='doctor-delete'),

    path('departments/', department_list_view, name='department-list'),
    path('departments/add/', department_create_view, name='department-create'),

    path('services/', service_list_view, name='service-list'),
    path('services/add/', service_create_view, name='service-create'),
    path('services/<int:pk>/', service_detail_view, name='service-detail'),
]
