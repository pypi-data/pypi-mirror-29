from django import forms
from django.forms import widgets
from django.template import loader
from django.utils.safestring import mark_safe


class StarSelect(widgets.RadioSelect):
    input_type = 'radio'
    template_name = 'materialize_nav/forms/widgets/star.html'
    option_template_name = 'materialize_nav/forms/widgets/star_option.html'

    first_on_deselect = True  # When you click to deselect your choice the first option is selected
    first_hidden = True   # The first option/choice is hidden and is selected on de-select
    ajax_post_url = None  # Post selection on click and get a response to may display the average or something

    def __init__(self, attrs=None, choices=()):
        if attrs is None:
            attrs = {}

        if "first_on_deselect" not in attrs:
            attrs["first_on_deselect"] =self.first_on_deselect
        if "first_hidden" not in attrs:
            attrs["first_hidden"] =self.first_hidden
        if "ajax_post_url" not in attrs:
            attrs["ajax_post_url"] =self.ajax_post_url

        super().__init__(attrs, choices)
