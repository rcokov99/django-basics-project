from django import forms
from specialists.models import Department, Service


class BootstrapFormMixin:
    """Automatically applies Bootstrap 5 classes to form widgets."""
    fields: dict

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            widget = field.widget
            if isinstance(widget, forms.CheckboxInput):
                widget.attrs['class'] = 'form-check-input'
            elif isinstance(widget, (forms.Select, forms.SelectMultiple)):
                widget.attrs['class'] = 'form-select'
            else:
                widget.attrs['class'] = 'form-control'


class DepartmentForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = Department
        fields = ['name', 'description']
        labels = {
            'name': 'Department Name',
            'description': 'Department Overview',
        }
        help_texts = {
            'name': 'Enter the official clinical department name (e.g., Cardiology, Pediatrics).',
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
            'price': 'Price ($)',
        }
        help_texts = {
            'name': 'Enter the name of the medical service or procedure.',
            'duration_minutes': 'Estimated duration of the service in minutes (minimum 5).',
            'price': 'Standard fee for this service in USD.',
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
        if duration is not None and duration < 5:
            raise forms.ValidationError('Service duration must be at least 5 minutes.')
        return duration