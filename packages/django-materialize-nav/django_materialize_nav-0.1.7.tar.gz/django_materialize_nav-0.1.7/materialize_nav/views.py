import collections
import copy
from django.db.models import CharField, TextField, Q, ForeignKey
from django.http import JsonResponse
from django.urls import reverse
from django.apps import apps
from django.views import generic
from django.core.paginator import Paginator
from django.views.generic.base import TemplateResponseMixin, ContextMixin, View, TemplateView
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.list import MultipleObjectMixin
import dynamicmethod

from .forms import SearchForm
from .utils import NavHeader, NavItem, list_property


__all__ = ["NavView", "NavSearch", "NavHeader", "NavItem", "SearchView"]


class NavSearch(object):
    pass


class TemplateMixin(TemplateResponseMixin, ContextMixin, View):
    """Make the view work like a regular template view."""
    def __init__(self, *args, **kwargs):
        if isinstance(self, MultipleObjectMixin) and not hasattr(self, "object_list"):
            self.object_list = None
        elif isinstance(self, SingleObjectMixin) and not hasattr(self, "object"):
            self.object = None
        super().__init__(*args, **kwargs)

    @classmethod
    def get_context(cls, request, context=None, **kwargs):
        if context is None:
            context = {}
        return context

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = self.get_context(self.request, context=context)
        return context

    def get(self, request, *args, **kwargs):
        if hasattr(super(), "get"):
            return super().get(request, *args, **kwargs)

        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)


class TitleViewMetaclass(type):
    """Meta class for resolving the set class Title and HomeURL.

    This meta class also checks the MRO for inheritance with template views.
    """

    def __init__(cls, name, bases, dct):
        if not any((hasattr(base, "get") for base in bases)):
            bases = (TemplateView,) + bases

        super(TitleViewMetaclass, cls).__init__(name, bases, dct)

        # ========== Defaults for the first NavView inherited item ==========
        if 'Title' in dct and dct["Title"]:
            try:
                if not NavView.Title:
                    NavView.Title = dct["Title"]
                if not NavView.DefaultTitle:
                    NavView.DefaultTitle = dct["Title"]
            except NameError:
                pass

        if "HomeURL" in dct and dct["HomeURL"]:
            try:
                if not NavView.HomeURL:
                    NavView.HomeURL = dct["HomeURL"]
            except NameError:
                pass

        if "NavColor" in dct and dct["NavColor"]:
            try:
                if not NavView.NavColor:
                    NavView.NavColor = dct["NavColor"]
            except NameError:
                pass

        if "SearchURL" in dct and dct["SearchURL"]:
            try:
                if not NavView.SearchURL:
                    NavView.SearchURL = dct["SearchURL"]
            except:
                pass

        if "SearchModels" in dct and dct["SearchModels"]:
            try:
                for model in dct["SearchModels"]:
                    NavView.SearchModels.append(model)
            except (NameError, TypeError):
                try:
                    NavView.SearchModels.append(dct["SearchModels"])
                except (NameError, TypeError):
                    pass


class FakeDict(object):
    def __init__(self, *args, **kwargs):
        self.d = dict(*args, **kwargs)

    def __getitem__(self, item):
        return self.d[item]

    def __setitem__(self, item, value):
        self.d[item] = value

    def __getattr__(self, item):
        return self.d[item]


class BaseNavOptions(object):
    @dynamicmethod
    def get_context(self, request, context=None, *, notification=None, **kwargs):
        if context is None:
            context = {}

        context['previous_page'] = request.META.get("HTTP_REFERER", '/')
        context['notification'] = request.GET.get("notification", notification)

        # Fake the request.user
        context['request'] = FakeDict(user=request.user, path=request.path)

        # Notify that the nav context was loaded
        request.nav_context_loaded = True

        return context


class TitleOptions(BaseNavOptions):
    AppName = ""
    DefaultTitle = ""
    Title = ""
    PageTitle = ""
    ShowPageTitle = False

    HomeURL = ""
    _HomeURL_CACHE_ = None

    def __init__(self, *args, app_name=None, title=None, page_title=None, show_page_title=None, home_url=None,
                 **kwargs):
        if app_name is not None:
            self.AppName = app_name
        if title is not None:
            self.Title = title
        if page_title is not None:
            self.PageTitle = page_title
        if show_page_title is not None:
            self.ShowPageTitle = show_page_title
        if home_url is not None:
            self.HomeURL = home_url

        super().__init__(*args, **kwargs)

    @dynamicmethod
    def get_context(self, request, context=None, *, title=None, page_title=None, show_page_title=None, home_url=None,
                    **kwargs):
        context = super().get_context(request, context=context, **kwargs)

        # Title
        if title is None:
            title = self.Title

        # Page Title
        if not page_title:
            page_title = self.PageTitle

        # Show page title
        if show_page_title is None:
            show_page_title = self.ShowPageTitle

        # Home url
        if home_url is None:
            home_url = self._HomeURL_CACHE_
        if not home_url:
            home_url = self.HomeURL
            try:
                home_url = reverse(home_url)
            except:
                try:
                    home_url = home_url.get_absolute_url()
                except:
                    pass
            self._HomeURL_CACHE_ = home_url

        context["AppName"] = self.AppName
        context['DefaultTitle'] = self.DefaultTitle
        context['Title'] = title
        context["PageTitle"] = page_title
        context["ShowPageTitle"] = show_page_title
        context['HomeURL'] = home_url

        return context


class NavBarOptions(BaseNavOptions):
    AppNavigation = collections.OrderedDict()
    NavItem = NavItem
    NavHeader = NavHeader
    NavColor = ""

    def __init__(self, *args, nav_color=None, nav_items=None, **kwargs):
        self.AppNavigation = self.get_app_navigation()

        if nav_color is not None:
            self.NavColor = nav_color
        if nav_items is not None:
            for item in nav_items:
                if isinstance(item, NavHeader) or len(item) == 1:
                    self.add_navigation_header(*item)
                else:
                    self.add_navigation(*item)

        super().__init__(*args, **kwargs)

    @dynamicmethod
    def add_navigation_header(self, app, icon=""):
        new_nav_header = self.NavHeader(app, icon)
        try:
            old_header = self.AppNavigation[new_nav_header.label]
            if not isinstance(old_header, self.NavHeader):
                old_header = self.NavHeader(old_header)
            old_header.extend(new_nav_header)
        except KeyError:
            self.AppNavigation[new_nav_header.label] = new_nav_header

    @dynamicmethod
    def add_navigation(self, url, label="", icon="", app="", url_args=None, url_kwargs=None):
        """Add a navigation item.

        Args:
            url (str/object): URL
            label (str)[""]: URL display name.
            icon (str)[None]: Material Icon name.
            app (str)["Inventory"]: App Group for dropdown. If app == "" it will be flat in the nav bar.
            url_args (tuple)[None]: Reverse url arguments.
            url_kwargs (dict)[None]: Reverse url key word arguments.
        """
        nav_item = self.NavItem(url, label, icon, url_args=url_args, url_kwargs=url_kwargs)
        if app:
            try:
                self.AppNavigation[app].append(nav_item)
            except:
                self.AppNavigation[app] = self.NavHeader(app, "", nav_item)
        else:
            app = label
            self.AppNavigation[app] = nav_item

    @dynamicmethod
    def get_app_navigation(self):
        """Return a copy of the AppNavigation. Override this for custom navigation for view instances."""
        return copy.deepcopy(self.AppNavigation)

    @dynamicmethod
    def get_context(self, request, nav_color=None, nav_items=None, **kwargs):
        """Return the context for the Navigation Bar and Navigation sidebar options.

        Args:
            request:
            nav_color (str): Navbar color.
            nav_items (list/tuple): List of list/NavItems and NavHeaders
            **kwargs:

        Returns:
            context(dict): View context
        """
        context = super().get_context(request, **kwargs)

        if nav_color is None:
            nav_color = self.NavColor or "teal"
        context["NavColor"] = nav_color

        if nav_items is not None:
            for item in nav_items:
                if isinstance(item, NavHeader) or len(item) == 1:
                    self.add_navigation_header(*item)
                else:
                    self.add_navigation(*item)
        context['AppNavigation'] = self.AppNavigation

        return context


class SearchOptions(BaseNavOptions):
    AppName = ""
    SearchURL = None
    _SearchURL_CACHE_ = None
    SearchModels = []

    def __init__(self, *args, app_name=None, search_url=None, search_models=None, **kwargs):
        if app_name is not None:
            self.AppName = app_name
        if search_url is not None:
            self.SearchURL = search_url
        if search_models is not None:
            self.SearchModels = search_models
        else:
            self.SearchModels = copy.deepcopy(self.__class__.SearchModels)

        super().__init__(*args, **kwargs)

    @dynamicmethod
    def add_search_model(self, model):
        if isinstance(model, (list, tuple)):
            for m in model:
                self.SearchModels.append(m)
        else:
            self.SearchModels.append(model)

    @dynamicmethod
    def get_search_models(self):
        return self.SearchModels

    @dynamicmethod
    def get_context(self, request, search_url=None, search_models=None, **kwargs):
        context = super().get_context(request, **kwargs)

        # Search url
        if search_url is None:
            search_url = self._SearchURL_CACHE_
            if not search_url:
                search_url = self.SearchURL
                try:
                    search_url = reverse(search_url)
                except:
                    try:
                        search_url = search_url.get_absolute_url()
                    except:
                        pass
                self._SearchURL_CACHE_ = search_url

        if search_models is None:
            search_models = self.get_search_models()

        # Search
        if search_url:
            try:
                app_name = " " + self.AppName
            except AttributeError:
                app_name = ""
            context["SearchURL"] = search_url
            context["SearchName"] = "Search" + app_name
            context["SearchFilters"] = [str(model._meta.model_name).strip() for model in search_models]
            context["SearchForm"] = SearchForm()

        return context


class SideBarOptions(SearchOptions):
    ShowSidebar = True
    FixedSidebar = True
    ContainerOn = True
    SidePanel = False

    def __init__(self, *args, show_sidebar=None, fixed_sidebar=None, container_on=None, side_panel=None, **kwargs):
        if show_sidebar is not None:
            self.ShowSidebar = show_sidebar
        if fixed_sidebar is not None:
            self.FixedSidebar = fixed_sidebar
        if container_on is not None:
            self.ContainerOn = container_on
        if side_panel is not None:
            self.SidePanel = side_panel

        super().__init__(*args, **kwargs)

    @dynamicmethod
    def get_context(self, request, context=None, show_sidebar=None, fixed_sidebar=None, container_on=None,
                    side_panel=None, **kwargs):
        context = super().get_context(request, context=context, **kwargs)

        if show_sidebar is None:
            show_sidebar = self.ShowSidebar
        if fixed_sidebar is None:
            fixed_sidebar = self.FixedSidebar
        if container_on is None:
            container_on = self.ContainerOn
        if side_panel is None:
            side_panel = self.SidePanel

        context["ShowSidebar"] = show_sidebar
        context["FixedSidebar"] = fixed_sidebar
        context["ContainerOn"] = container_on
        context["SidePanel"] = side_panel

        return context


class NavView(SideBarOptions, SearchOptions, NavBarOptions, TitleOptions, BaseNavOptions,
              TemplateMixin, metaclass=TitleViewMetaclass):
    """Standard view for navigation items and other view defaults."""

    AppName = ""
    DefaultTitle = ""
    Title = ""
    PageTitle = ""
    ShowPageTitle = False
    HomeURL = ""

    AppNavigation = collections.OrderedDict()
    NavItem = NavItem
    NavHeader = NavHeader
    NavColor = ""  # "teal" is default

    ShowSidebar = True
    FixedSidebar = True
    ContainerOn = True
    SidePanel = False

    SearchURL = None
    SearchModels = []

    @dynamicmethod
    def get_context(self, request, context=None, title=None, page_title=None, show_page_title=None, home_url=None,
                    nav_color=None, nav_items=None,
                    show_sidebar=None, fixed_sidebar=None, container_on=None, side_panel=None, search_url=None,
                    search_models=None, notification=None, **kwargs):
        return super().get_context(request, context=context, title=title, page_title=page_title,
                                   show_page_title=show_page_title, home_url=home_url,
                                   nav_color=nav_color, nav_items=nav_items,
                                   show_sidebar=show_sidebar, fixed_sidebar=fixed_sidebar, container_on=container_on,
                                   side_panel=side_panel,
                                   search_url=search_url, search_models=search_models,
                                   notification=notification, **kwargs)


class SearchView(NavView):
    """Search through multiple models.

    Still need to think this one through a little bit. The SearchForm seems pointless.

    Note:
        search_results contains a list of list of SearchResult's.
            Ex. [SearchResult(QuerySet, Model, "Searched Text"), SearchResult(QuerySet, Model, "Searched Text")],]

    Note:
        If Ajax is used this returns the json object which is a list of [[String value, URL]].
        {search_results: [["[Model] value1", url1], ["[Model 2] value2", url2]]}
    """
    PageTitle = "Search Results"
    template_name = 'materialize_nav/search_results.html'
    context_object_name = 'search_results'
    search_form = SearchForm
    paginate_by = 10

    @dynamicmethod
    def add_search_model(self, model):
        return self.add_search_model(model)

    @dynamicmethod
    def get_search_models(self):
        return self.get_search_models()

    def get_context_object_name(self):
        """Get the name of the item to be used in the context."""
        if self.context_object_name:
            return self.context_object_name
        return "search_results"

    @classmethod
    def get_object_url(cls, obj):
        try:
            return obj.get_absolute_url()
        except:
            return ""

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.method == "GET":
            request_dict = self.request.GET
        else:
            request_dict = self.request.POST

        # search_form = self.search_form(request_dict)
        search_results = self.search_form.get_search_results(request_dict["search"], request_dict["filters"],
                                                             self.get_search_models())
        context[self.get_context_object_name()] = search_results

        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        if request.is_ajax():
            context_name = self.get_context_object_name()
            li = []
            for sr in context[context_name]:
                li.extend([[str(res) + " [" + str(sr.model) + "]", self.get_object_url(res)]
                           for res in sr.results[: self.paginate_by]])
            return JsonResponse({context_name: li}, status=200)
        else:
            return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        if request.is_ajax():
            context_name = self.get_context_object_name()
            li = []
            for sr in context[context_name]:
                li.extend([[str(res) + " [" + str(sr.model) + "]", self.get_object_url(res)]
                           for res in sr.results[: self.paginate_by]])
            return JsonResponse({context_name: li}, status=200)
        else:
            return self.render_to_response(context)
