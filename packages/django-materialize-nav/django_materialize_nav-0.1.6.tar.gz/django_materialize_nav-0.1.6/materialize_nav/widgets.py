from django import forms
from django.db.models import Avg
from django.forms import widgets
from django.template import loader
from django.utils.safestring import mark_safe

from .utils import get_star_type


class StarSelectWidget(widgets.RadioSelect):
    input_type = 'radio'
    template_name = 'materialize_nav/forms/widgets/stars.html'
    option_template_name = 'materialize_nav/forms/widgets/star_option.html'

    class Media:
        js = ('materialize_nav/stars.js',)

    def __init__(self, attrs=None, choices=(), ranking=None, color="yellow", select_color="blue"):
        self.color = color
        self.select_color = select_color
        self.ranking = ranking
        self._qs = None
        super().__init__(attrs=attrs, choices=choices)

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        context['widget']["color"] = self.color
        context['widget']["select_color"] = self.select_color
        context['widget']["ranking"] = self.ranking or 0
        context["widget"]["stars"] = [get_star_type(i, self.ranking or 0) for i in range(len(self.choices))]
        return context

    def create_option(self, name, value, label, selected, index, subindex=None, attrs=None):
        context = super().create_option(name, value, label, selected, index, subindex=subindex, attrs=attrs)
        context["star_ranking_class"] = get_star_type(index, self.ranking or 0)
        context["color"] = self.color
        return context

    def render(self, name, value, attrs=None, renderer=None):
        """Render the widget as an HTML string."""
        context = self.get_context(name, value, attrs)
        return self._render(self.template_name, context, renderer)
