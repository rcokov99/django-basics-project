from django.db.models import Avg, Count, F, Q
from django.shortcuts import get_object_or_404, redirect, render

from specialists.forms import DepartmentForm
from specialists.models import Department, Doctor


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


# --- DEPARTMENT VIEWS ---


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
