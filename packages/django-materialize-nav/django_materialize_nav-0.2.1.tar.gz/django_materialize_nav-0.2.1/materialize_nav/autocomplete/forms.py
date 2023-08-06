from django import forms

from .widgets import AutocompleteWidget


__all__ = ['StarSelectField', 'AutocompleteWidget']


class StarSelectField(forms.ModelChoiceField):
    widget = AutocompleteWidget

    def __init__(self, queryset=(), url=None, url_args=None, url_kwargs=None, *args, **kwargs):
        if "label" not in kwargs:
            kwargs["label"] = ''

        if "widget" not in kwargs:
            kwargs['widget'] = self.widget(url=url, url_args=url_args, url_kwargs=url_kwargs)
        super().__init__(*args, **kwargs)
