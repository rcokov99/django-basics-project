from django.db.models import Avg, F
from django.shortcuts import render
from specialists.models import Doctor, Department
from appointments.models import Appointment


def home_view(request):
    top_doctors = (
        Doctor.objects
        .select_related('department')
        .annotate(avg_rating=Avg('reviews__rating'))
        .order_by(F('avg_rating').desc(nulls_last=True), '-years_of_experience', 'full_name')[:3]
    )

    context = {
        'doctor_count': Doctor.objects.count(),
        'department_count': Department.objects.count(),
        'appointment_count': Appointment.objects.count(),
        'top_doctors': top_doctors,
    }
    return render(request, 'common/home.html', context)