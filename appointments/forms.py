from django import forms
from django.utils import timezone
from appointments.models import Appointment
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
                    'min': '08:00',
                    'max': '17:00',
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

    def clean_appointment_date_time(self):
        appt_time = self.cleaned_data.get('appointment_date_time')
        if appt_time:
            if appt_time < timezone.now():
                raise forms.ValidationError('Appointment date and time cannot be in the past.')
            if appt_time.hour < 8 or appt_time.hour > 17 or (appt_time.hour == 17 and appt_time.minute > 0):
                raise forms.ValidationError('Appointments must be scheduled between 08:00 and 17:00.')
        return appt_time


class AppointmentDeleteForm(AppointmentForm):
    """Read-only variant of AppointmentForm for deletion confirmations."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.disabled = True
