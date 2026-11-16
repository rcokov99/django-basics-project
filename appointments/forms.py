from datetime import timedelta
from django import forms
from django.utils import timezone
from appointments.models import Appointment
from specialists.models import Doctor, Service
from common.forms import BootstrapFormMixin


class AppointmentForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['doctor', 'service', 'patient_name', 'patient_email', 'appointment_date_time']
        labels = {
            'doctor': 'Doctor',
            'service': 'Service',
            'patient_name': 'Patient Name',
            'patient_email': 'Patient Email',
            'appointment_date_time': 'Appointment Date & Time',
        }
        help_texts = {
            'doctor': 'Select the doctor for this consultation.',
            'service': 'Select the type of medical service needed.',
            'patient_name': 'Enter the full name of the patient.',
            'patient_email': 'Enter a contact email for appointment notifications.',
            'appointment_date_time': 'Choose a future date and time for the visit (08:00 - 17:00).',
        }
        widgets = {
            'doctor': forms.Select(attrs={'class': 'form-select'}),
            'service': forms.Select(attrs={'class': 'form-select'}),
            'patient_name': forms.TextInput(attrs={
                'placeholder': 'e.g., Jane Doe',
            }),
            'patient_email': forms.EmailInput(attrs={
                'placeholder': 'e.g., jane@example.com',
            }),
            'appointment_date_time': forms.DateTimeInput(
                attrs={
                    'type': 'datetime-local',
                    'class': 'form-control',
                    'style': 'line-height: 1.2; padding-top: 0.375rem; padding-bottom: 0.375rem;',
                },
                format='%Y-%m-%dT%H:%M',
            ),
        }
        error_messages = {
            'doctor': {
                'required': 'Please select a doctor.',
            },
            'service': {
                'required': 'Please select a service.',
            },
            'patient_name': {
                'required': 'Please enter the patient name.',
            },
            'patient_email': {
                'required': 'Please enter a patient email.',
                'invalid': 'Enter a valid email address.',
            },
            'appointment_date_time': {
                'required': 'Please specify the appointment date and time.',
                'invalid': 'Enter a valid date and time format.',
            },
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['doctor'].empty_label = 'Select a doctor'
        self.fields['service'].empty_label = 'Select a service'

        self.fields['service'].queryset = Service.objects.none()

        doctor_id = None

        if self.data and self.data.get('doctor'):
            doctor_id = self.data.get('doctor')
        elif self.initial and self.initial.get('doctor'):
            doctor_id = self.initial.get('doctor')
        elif self.instance and self.instance.pk and self.instance.doctor_id:
            doctor_id = self.instance.doctor_id

        if doctor_id:
            try:
                doctor = Doctor.objects.get(pk=doctor_id)
                if hasattr(doctor, 'services'):
                    self.fields['service'].queryset = doctor.services.all()
                elif hasattr(Service, 'doctors'):
                    self.fields['service'].queryset = Service.objects.filter(doctors=doctor)
                else:
                    self.fields['service'].queryset = Service.objects.all()
            except Doctor.DoesNotExist:
                pass

    def clean_appointment_date_time(self):
        appt_time = self.cleaned_data.get('appointment_date_time')
        if appt_time:
            if appt_time < timezone.now():
                raise forms.ValidationError('Appointment date and time cannot be in the past.')
            if appt_time.hour < 8 or appt_time.hour > 17 or (appt_time.hour == 17 and appt_time.minute > 0):
                raise forms.ValidationError('Appointments must be scheduled between 08:00 and 17:00.')
        return appt_time

    def clean(self):
        cleaned_data = super().clean()
        doctor = cleaned_data.get('doctor')
        service = cleaned_data.get('service')
        appt_time = cleaned_data.get('appointment_date_time')

        if doctor and service and appt_time:
            duration = timedelta(minutes=service.duration_minutes)
            appt_end_time = appt_time + duration

            overlapping_appointments = Appointment.objects.filter(doctor=doctor)
            if self.instance and self.instance.pk:
                overlapping_appointments = overlapping_appointments.exclude(pk=self.instance.pk)

            for existing in overlapping_appointments:
                existing_start = existing.appointment_date_time
                existing_duration = timedelta(minutes=existing.service.duration_minutes)
                existing_end = existing_start + existing_duration

                if appt_time < existing_end and appt_end_time > existing_start:
                    raise forms.ValidationError(
                        f"Dr. {doctor.full_name} already has an overlapping appointment "
                        f"scheduled from {existing_start.strftime('%H:%M')} to {existing_end.strftime('%H:%M')}."
                    )

        return cleaned_data


class AppointmentDeleteForm(AppointmentForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.disabled = True
