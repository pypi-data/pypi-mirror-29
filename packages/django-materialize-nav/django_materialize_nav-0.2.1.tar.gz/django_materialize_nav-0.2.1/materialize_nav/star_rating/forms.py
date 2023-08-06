from django import forms

from .widgets import StarSelectWidget


__all__ = ['StarSelectField', 'StarSelectWidget']


class StarSelectField(forms.ChoiceField):
    widget = StarSelectWidget

    def __init__(self, *args, **kwargs):
        if "label" not in kwargs:
            kwargs["label"] = ''
        super().__init__(*args, **kwargs)
