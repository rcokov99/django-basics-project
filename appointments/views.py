from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from appointments.forms import AppointmentForm, AppointmentDeleteForm
from appointments.models import Appointment
from specialists.models import Doctor


def appointment_list_view(request):
    appointments = Appointment.objects.select_related('doctor','service')

    doctor_id = request.GET.get('doctor', '')
    status_filter = request.GET.get('status', '')

    if doctor_id and doctor_id.isdigit():
        appointments = appointments.filter(doctor_id=doctor_id)

    now = timezone.now()
    if status_filter == 'upcoming':
        appointments = appointments.filter(appointment_date_time__gte=now)
    elif status_filter == 'past':
        appointments = appointments.filter(appointment_date_time__lt=now)

    appointments = appointments.order_by('appointment_date_time')

    context = {
        'appointments': appointments,
        'doctors': Doctor.objects.all(),
        'selected_doctor': doctor_id,
        'selected_status': status_filter,
        'now': now,
    }
    return render(request, 'appointments/appointment_list.html', context)


def appointment_create_view(request):
    initial = {}
    doctor_id = request.GET.get('doctor')
    service_id = request.GET.get('service')
    if doctor_id and doctor_id.isdigit():
        initial['doctor'] = doctor_id
    if service_id and service_id.isdigit():
        initial['service'] = service_id
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('appointments:appointment-list')
    else:
        form = AppointmentForm(initial=initial)

    context = {
        'form': form,
        'doctors_exist': Doctor.objects.exists(),
    }
    return render(request, 'appointments/appointment_form.html', context)


def appointment_edit_view(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk)
    if request.method == 'POST':
        form = AppointmentForm(request.POST, instance=appointment)
        if form.is_valid():
            form.save()
            return redirect('appointments:appointment-list')
    else:
        form = AppointmentForm(instance=appointment)

    context = {
        'form': form,
        'appointment': appointment,
        'doctors_exist': Doctor.objects.exists(),
    }
    return render(request, 'appointments/appointment_form.html', context)


def appointment_delete_view(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk)
    if request.method == 'POST':
        appointment.delete()
        return redirect('appointments:appointment-list')

    form = AppointmentDeleteForm(instance=appointment)
    context = {
        'form': form,
        'appointment': appointment,
    }
    return render(request, 'appointments/appointment_delete.html', context)
