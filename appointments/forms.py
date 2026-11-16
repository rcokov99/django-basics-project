from datetime import time, timedelta
from django import forms
from django.utils import timezone
from appointments.models import Appointment
from specialists.models import Doctor, Service
from common.forms import BootstrapFormMixin
from django.core.exceptions import NON_FIELD_ERRORS


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
            'doctor': forms.Select(),
            'service': forms.Select(),
            'patient_name': forms.TextInput(attrs={
                'placeholder': 'e.g., Jane Doe',
            }),
            'patient_email': forms.EmailInput(attrs={
                'placeholder': 'e.g., jane@example.com',
            }),
            'appointment_date_time': forms.DateTimeInput(
                attrs={
                    'type': 'datetime-local',
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
            NON_FIELD_ERRORS: {
                'unique_together': 'This doctor is already booked at this date and time. Please choose a different time.',
            },
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['doctor'].empty_label = 'Select a doctor'
        self.fields['service'].empty_label = 'Select a service'

    def clean_appointment_date_time(self):
        appt_time = self.cleaned_data.get('appointment_date_time')
        if appt_time:
            if appt_time < timezone.now():
                raise forms.ValidationError('Appointment date and time cannot be in the past.')

            appt_time_only = appt_time.time()
            if appt_time_only < time(8, 0) or appt_time_only > time(17, 0):
                raise forms.ValidationError('Appointments must be scheduled between 08:00 and 17:00.')
        return appt_time

    def clean(self):
        cleaned_data = super().clean()
        doctor = cleaned_data.get('doctor')
        service = cleaned_data.get('service')
        appt_time = cleaned_data.get('appointment_date_time')

        if doctor and service:
            if not doctor.services.filter(pk=service.pk).exists():
                self.add_error('service', 'This doctor does not offer the selected service.')
                return cleaned_data

        if doctor and service and appt_time:
            duration = timedelta(minutes=service.duration_minutes)
            appt_end_time = appt_time + duration

            overlapping_appointments = Appointment.objects.filter(doctor=doctor).select_related('service')
            if self.instance and self.instance.pk:
                overlapping_appointments = overlapping_appointments.exclude(pk=self.instance.pk)

            for existing in overlapping_appointments:
                existing_start = existing.appointment_date_time

                if appt_time == existing_start:
                    continue

                existing_end = existing_start + timedelta(minutes=existing.service.duration_minutes)

                if appt_time < existing_end and appt_end_time > existing_start:
                    local_start = timezone.localtime(existing_start)
                    local_end = timezone.localtime(existing_end)
                    raise forms.ValidationError(
                        f"Dr. {doctor.full_name} already has an overlapping appointment "
                        f"scheduled from {local_start.strftime('%H:%M')} to {local_end.strftime('%H:%M')}."
                    )

        return cleaned_data


class AppointmentDeleteForm(AppointmentForm):
    """Form used for confirming and deleting an existing appointment."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.disabled = True
