from django.urls import path
from specialists.views import doctor_list_view, doctor_detail_view

app_name = 'specialists'

urlpatterns = [
    path('', doctor_list_view, name='doctor-list'),
    path('<int:pk>/', doctor_detail_view, name='doctor-detail'),
]