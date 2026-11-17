from django import forms
from specialists.models import Department, Service, Doctor
from common.forms import BootstrapFormMixin


class DepartmentForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = Department
        fields = ['name', 'description']
        labels = {
            'name': 'Department Name',
            'description': 'Department Overview',
        }
        help_texts = {
            'name': 'Enter the official clinical department name (e.g., Cardiology, Neurology).',
            'description': 'Briefly summarize the conditions treated and care provided in this department.',
        }
        widgets = {
            'name': forms.TextInput(attrs={
                'placeholder': 'e.g., Cardiology',
            }),
            'description': forms.Textarea(attrs={
                'placeholder': 'Describe the focus and scope of this department...',
                'rows': 4,
            }),
        }
        error_messages = {
            'name': {
                'required': 'Please enter a department name.',
                'unique': 'A department with this name already exists.',
            },
        }

    def clean_name(self):
        name = self.cleaned_data.get('name', '').strip()
        if name.isdigit():
            raise forms.ValidationError('Department name cannot consist solely of numbers.')

        if Department.objects.filter(name__iexact=name).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError('A department with this name already exists.')

        return name


class ServiceForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = Service
        fields = ['name', 'description', 'duration_minutes', 'price']
        labels = {
            'name': 'Service Name',
            'description': 'Service Description',
            'duration_minutes': 'Duration (Minutes)',
            'price': 'Price (€)',
        }
        help_texts = {
            'name': 'Enter the name of the medical service or procedure.',
            'duration_minutes': 'Estimated duration of the service in minutes (minimum 5).',
            'price': 'Standard fee for this service in EUR€.',
        }
        widgets = {
            'name': forms.TextInput(attrs={
                'placeholder': 'e.g., General Consultation',
            }),
            'description': forms.Textarea(attrs={
                'placeholder': 'Provide details about what this service entails...',
                'rows': 4,
            }),
            'duration_minutes': forms.NumberInput(attrs={
                'placeholder': 'e.g., 30',
                'min': '5',
            }),
            'price': forms.NumberInput(attrs={
                'placeholder': 'e.g., 99.00',
                'step': '0.01',
            }),
        }
        error_messages = {
            'name': {
                'required': 'Please enter a service name.',
            },
            'duration_minutes': {
                'required': 'Please specify the duration.',
                'invalid': 'Enter a valid number for duration.',
            },
            'price': {
                'required': 'Please specify a price.',
                'invalid': 'Enter a valid price amount.',
            },
        }

    def clean_name(self):
        name = self.cleaned_data.get('name', '').strip()
        if name.isdigit():
            raise forms.ValidationError('Service name cannot consist solely of numbers.')

        if Service.objects.filter(name__iexact=name).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError('A service with this name already exists.')

        return name

    def clean_duration_minutes(self):
        duration = self.cleaned_data.get('duration_minutes')
        if duration is None:
            return duration
        if duration < 5:
            raise forms.ValidationError('Service duration must be at least 5 minutes.')
        return duration


class DoctorForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = Doctor
        fields = ['full_name', 'department', 'specialty', 'years_of_experience', 'bio', 'services']
        labels = {
            'full_name': 'Full Name',
            'department': 'Department',
            'specialty': 'Specialty',
            'years_of_experience': 'Years of Experience',
            'bio': 'Biography',
            'services': 'Offered Services',
        }
        help_texts = {
            'full_name': 'Enter the doctor’s full professional name without "Dr." (letters, spaces, dots, hyphens, and apostrophes).',
            'department': 'Select the clinical department this doctor belongs to.',
            'specialty': 'Specific area of expertise within the department',
            'years_of_experience': 'Total years practicing medicine (maximum 60).',
            'bio': 'Provide a short professional biography and background overview.',
            'services': 'Select all medical services this specialist provides.',
        }
        widgets = {
            'full_name': forms.TextInput(attrs={
                'placeholder': 'e.g., John Smith',
            }),
            'department': forms.Select(),
            'specialty': forms.TextInput(attrs={
                'placeholder': 'e.g., Pediatric Cardiologist',
            }),
            'years_of_experience': forms.NumberInput(attrs={
                'placeholder': 'e.g., 10',
                'min': '0',
                'max': '60',
            }),
            'bio': forms.Textarea(attrs={
                'placeholder': 'Write a brief professional background and clinical focus...',
                'rows': 4,
            }),
            'services': forms.CheckboxSelectMultiple(),
        }
        error_messages = {
            'full_name': {
                'required': 'Please enter the doctor’s full name.',
            },
            'department': {
                'required': 'Please select a department.',
            },
            'specialty': {
                'required': 'Please specify a specialty.',
            },
            'years_of_experience': {
                'required': 'Please specify years of experience.',
                'invalid': 'Enter a valid number for experience.',
            },
            'services': {
                'required': 'Please select at least one service.',
            },
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['department'].empty_label = 'Select a department'
        self.fields['services'].required = True

    def clean_full_name(self):
        full_name = self.cleaned_data.get('full_name', '').strip()

        if full_name.lower().startswith(('dr.', 'dr ')):
            raise forms.ValidationError('Please enter the name without the "Dr." prefix.')

        allowed_symbols = " .'-"
        if not all(char.isalpha() or char in allowed_symbols for char in full_name):
            raise forms.ValidationError('Full name can only contain letters, spaces, dots, hyphens and apostrophes.')

        return full_name

    def clean_years_of_experience(self):
        years = self.cleaned_data.get('years_of_experience')
        if years is not None and years > 60:
            raise forms.ValidationError('Years of experience cannot exceed 60.')
        return years


class DoctorDeleteForm(DoctorForm):
    """Read-only variant of DoctorForm used for confirmation views prior to deletion."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.disabled = True
