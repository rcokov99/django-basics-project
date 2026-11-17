from django.db.models import Avg, Count, F, Q
from django.shortcuts import get_object_or_404, redirect, render

from specialists.forms import (
    DepartmentForm,
    ServiceForm,
    DoctorForm,
    DoctorDeleteForm,
)
from specialists.models import Department, Doctor, Service


def doctor_list_view(request):
    doctors = Doctor.objects.select_related('department').annotate(
        avg_rating=Avg('reviews__rating')
    )

    search_query = request.GET.get('q', '').strip()
    department_id = request.GET.get('department', '')
    sort_by = request.GET.get('sort', '')

    if search_query:
        doctors = doctors.filter(
            Q(full_name__icontains=search_query)
            | Q(specialty__icontains=search_query)
        )

    if department_id and department_id.isdigit():
        doctors = doctors.filter(department_id=department_id)

    sort_mapping = {
        'experience': ('-years_of_experience', 'full_name'),
        'rating': (F('avg_rating').desc(nulls_last=True), 'full_name'),
        'name': ('full_name',),
    }

    order_expressions = sort_mapping.get(sort_by, ('full_name',))
    doctors = doctors.order_by(*order_expressions)

    context = {
        'doctors': doctors,
        'departments': Department.objects.all(),
        'search_query': search_query,
        'selected_department': department_id,
        'selected_sort': sort_by,
    }
    return render(request, 'specialists/doctor_list.html', context)


def doctor_detail_view(request, pk):
    doctor = get_object_or_404(
        Doctor.objects.select_related('department').prefetch_related(
            'services', 'reviews', 'appointments'
        ),
        pk=pk,
    )
    return render(request, 'specialists/doctor_detail.html', {'doctor': doctor})


def doctor_create_view(request):
    if request.method == 'POST':
        form = DoctorForm(request.POST)
        if form.is_valid():
            doctor = form.save()
            return redirect('specialists:doctor-detail', pk=doctor.pk)
    else:
        form = DoctorForm()

    context = {
        'form': form,
        'departments_exist': Department.objects.exists(),
        'services_exist': Service.objects.exists(),
    }
    return render(request, 'specialists/doctor_form.html', context)


def doctor_edit_view(request, pk):
    doctor = get_object_or_404(Doctor, pk=pk)
    if request.method == 'POST':
        form = DoctorForm(request.POST, instance=doctor)
        if form.is_valid():
            form.save()
            return redirect('specialists:doctor-detail', pk=doctor.pk)
    else:
        form = DoctorForm(instance=doctor)

    context = {
        'form': form,
        'doctor': doctor,
        'departments_exist': Department.objects.exists(),
        'services_exist': Service.objects.exists(),
    }
    return render(request, 'specialists/doctor_form.html', context)


def doctor_delete_view(request, pk):
    doctor = get_object_or_404(Doctor, pk=pk)
    if request.method == 'POST':
        doctor.delete()
        return redirect('specialists:doctor-list')

    form = DoctorDeleteForm(instance=doctor)
    context = {
        'form': form,
        'doctor': doctor,
    }
    return render(request, 'specialists/doctor_delete.html', context)


def department_list_view(request):
    departments = Department.objects.annotate(
        doctor_total=Count('doctors')
    ).order_by('name')

    context = {
        'departments': departments,
    }
    return render(request, 'specialists/department_list.html', context)


def department_create_view(request):
    if request.method == 'POST':
        form = DepartmentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('specialists:department-list')
    else:
        form = DepartmentForm()

    context = {
        'form': form,
    }
    return render(request, 'specialists/department_form.html', context)


def service_list_view(request):
    services = Service.objects.annotate(
        doctor_total=Count('doctors')
    ).order_by('name')

    context = {
        'services': services,
    }
    return render(request, 'specialists/service_list.html', context)


def service_create_view(request):
    if request.method == 'POST':
        form = ServiceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('specialists:service-list')
    else:
        form = ServiceForm()

    context = {
        'form': form,
    }
    return render(request, 'specialists/service_form.html', context)


def service_detail_view(request, pk):
    service = get_object_or_404(
        Service.objects.prefetch_related('doctors'),
        pk=pk,
    )
    context = {
        'service': service,
    }
    return render(request, 'specialists/service_detail.html', context)
