# Django Materialize Nav
This library was created to make django work with materializecss. This library primarily focuses on the 
navbar and sidebar display and navigation.

See the work_place_things for example usage

## Setup
Install the library.


```python
# project/settings.py

INSTALLED_APPS = [
    "materialize_nav",
    ...
]

# If you want this library to override django form widget templates
INSTALLED_APPS.append('django.forms')
FORM_RENDERER = 'django.forms.renderers.TemplatesSetting'

```

Get the standard context for views
```python
# views.py

from materialize_nav import NavView


class MyView(NavView):  # NavView is a simple TemplateView
    template_name = "my_page.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

# or

def show_page(request)
    context = NavView.get_context(request, title="My Page")
    context["object"] = "MyObject"
    return render(request, "my_page.html", context)
```


## Basics
This library mostly works with class based views.
