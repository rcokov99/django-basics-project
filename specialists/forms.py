from django import forms
from specialists.models import Department


class BootstrapFormMixin:
    """Automatically applies Bootstrap 5 classes to form widgets."""

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
                'max_length': 'The department name is too long.',
            },
        }

    def clean_name(self):
        name = self.cleaned_data.get('name', '').strip()
        if name.isdigit():
            raise forms.ValidationError('Department name cannot consist solely of numbers.')

        if Department.objects.filter(name__iexact=name).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError('A department with this name already exists.')

        return name