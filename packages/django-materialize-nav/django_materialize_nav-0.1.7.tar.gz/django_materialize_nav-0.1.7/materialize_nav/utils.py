import requests
import urllib
from django.shortcuts import redirect
from django.urls import reverse

import os

import math

__all__ = ["list_property", "NavHeader", "NavItem", 'SearchResult', 'nav_redirect', 'image_exists', 'get_star_type']


class list_property(property):
    """Property that is really just a list index."""
    def __init__(self, index=None, default=ValueError("Invalid list_property value"),
                 fget=None, fset=None, fdel=None, doc=None):
        """Property that is really just a list index

        Args:
            index (int): The list index position associated with this property
            default (object)[ValueError]: The default value or Exception when the index/value has not been set.
            fget (function)[None]: Getter function
            fset (function)[None]: Setter function
            fdel (function)[None]: Deleter function
            doc (str)[None]: Documentation

        Alt Args:
            fget (function)[None]: Getter function
            fset (function)[None]: Setter function
            fdel (function)[None]: Deleter function
            doc (str)[None]: Documentation
            index (int): The list index position associated with this property
            default (object)[ValueError]: The default value or Exception when the index/value has not been set.
        """
        # Swap arguments
        if not isinstance(index, int):
            fget, index = index, None
            if callable(default):
                fset, default = default, None

        self.index = index
        self.default = default

        if fget is None:
            fget = self.get_value
        if fset is None:
            fset = self.set_value

        super().__init__(fget, fset, fdel, doc)

    def getter(self, fget):
        return type(self)(self.index, self.default, fget, self.fset, self.fdel, self.__doc__)

    def setter(self, fset):
        return type(self)(self.index, self.default, self.fget, fset, self.fdel, self.__doc__)

    def deleter(self, fdel):
        return type(self)(self.index, self.default, self.fget, self.fset, fdel, self.__doc__)

    def __call__(self, fget):
        return self.getter(fget)

    def get_value(self, obj):
        try:
            return obj[self.index]
        except Exception as err:
            if isinstance(self.default, Exception):
                raise self.default from err
            return self.default

    def set_value(self, obj, value):
        try:
            obj[self.index] = value
            return
        except IndexError:
            while len(obj) < self.index+1:
                obj.append(None)
        obj[self.index] = value

    def del_value(self, obj):
        try:
            obj.pop(self.index)
        except IndexError:
            pass


class NavHeader(list):
    def __init__(self, label, icon="", *args):
        if isinstance(label, NavHeader):
            icon = label.icon
            label = label.label
        elif isinstance(label, NavItem):
            icon = label.icon
            label = label.label
        super().__init__(*args)

        self.label = label
        self.icon = icon

    def is_header(self):
        return True

    def get_nav_items(self):
        return self[:]


class NavItem(list):
    url = list_property(0, "")
    label = list_property(1, "")
    icon = list_property(2, "")
    app = list_property(3, None)
    url_args = list_property(4, None)
    url_kwargs = list_property(5, None)

    def __init__(self, url, label="", icon="", app=None, url_args=None, url_kwargs=None, *args):
        if isinstance(url, NavItem):
            icon = url.icon
            label = url.label
            app = url.app
            url_args = url.url_args
            url_kwargs = url.url_kwargs
            url = url.url

        super().__init__((url, label, icon, app, url_args, url_kwargs) + args)
        if url_args is None:
            url_args = []
        if url_kwargs is None:
            url_kwargs = {}
        self.url_args = url_args
        self.url_kwargs = url_kwargs

    @url.getter
    def url(self):
        try:
            url = self[0]
        except:
            url = ""

        try:
            url = reverse(url, args=self.url_args, kwargs=self.url_kwargs)
        except:
            try:
                url = url.get_absolute_url()
            except:
                pass
        return url

    def is_header(self):
        return False


class SearchResult(list):
    """Search results. Stores information about a search.

    Args:
        results (QuerySet): Result queryset
        model (str): Model name.
        search_text (str): Test that was used in the search.
    """
    results = list_property(0, [])
    model = list_property(1, None)
    search_text = list_property(2, "")

    def __init__(self, results, model, search_text):
        super().__init__((results, model, search_text))


def nav_redirect(*args, get_params=None, **kwargs):
    """Redirect to a view and give optional get parameters.

    Args:
        *args: Normal redirect arguments
        get_params (dict)[None]: Dictionary of get paramters.
        **kwargs: Normal redirect key word arguments
    """
    response = redirect(*args, **kwargs)
    if get_params:
        try:
            params = urllib.parse.urlencode(get_params)
        except AttributeError:
            params = urllib.urlencode(get_params)
        response["Location"] += "?%s" % params
    return response


def image_exists(image_path):
    """Return if an image or file exists."""
    image_path = str(image_path)
    try:
        r = requests.get(image_path)
        return r.status_code == 200
    except:
        if os.path.exists(image_path) or (os.path.exists("." + image_path) and os.path.isfile("." + image_path)):
            return True
        return False


def get_star_type(index, ranking):
    """Return the icon class name for the given star index and average ranking."""
    if ranking < index or (ranking == 0 and index == 0):
        return "star_border_icon"
    elif math.floor(ranking) > index or (ranking % 1 == 0 and ranking == index):
        return "star_icon"
    else:
        return "star_half_icon"
