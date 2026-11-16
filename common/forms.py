from django import forms

class BootstrapFormMixin:
    """Automatically applies Bootstrap 5 classes to form widgets."""
    fields: dict

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            widget = field.widget
            if isinstance(widget, forms.CheckboxInput):
                widget.attrs['class'] = 'form-check-input'
            elif isinstance(widget, forms.CheckboxSelectMultiple):
                widget.attrs['class'] = 'checkbox-list'
            elif isinstance(widget, (forms.Select, forms.SelectMultiple)):
                widget.attrs['class'] = 'form-select'
            else:
                widget.attrs['class'] = 'form-control'