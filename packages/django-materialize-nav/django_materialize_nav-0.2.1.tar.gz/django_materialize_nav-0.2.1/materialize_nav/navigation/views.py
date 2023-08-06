import collections
from django.views.generic import TemplateView
from dynamicmethod import dynamicmethod

from .utils import NavHeader, NavItem
from .template_mixin import TemplateMixin

from . import nav_option_views
from ..search.nav_option_views import SearchOptions


__all__ = ['TemplateMixin', 'NavHeader', 'NavItem', 'TitleViewMetaclass', 'BaseNavOptions', 'TitleOptions',
           'NavBarOptions', 'SideBarOptions', 'SearchOptions', 'NavView']


BaseNavOptions = nav_option_views.BaseNavOptions
TitleOptions = nav_option_views.TitleOptions
NavBarOptions = nav_option_views.NavBarOptions
SideBarOptions = nav_option_views.SideBarOptions


class TitleViewMetaclass(type):
    """Meta class for resolving the set class Title and HomeURL.

    This meta class also checks the MRO for inheritance with template views.
    """
    BASE_NAV_VIEW = None

    def __init__(cls, name, bases, dct):
        if not any((hasattr(base, "get") for base in bases)):
            bases = (TemplateView,) + bases

        super(TitleViewMetaclass, cls).__init__(name, bases, dct)

        # ========== Defaults for the first NavView inherited item ==========
        if 'Title' in dct and dct["Title"]:
            try:
                if not cls.BASE_NAV_VIEW.Title:
                    cls.BASE_NAV_VIEW.Title = dct["Title"]
                if not cls.BASE_NAV_VIEW.DefaultTitle:
                    cls.BASE_NAV_VIEW.DefaultTitle = dct["Title"]
            except NameError:
                pass

        if "HomeURL" in dct and dct["HomeURL"]:
            try:
                if not cls.BASE_NAV_VIEW.HomeURL:
                    cls.BASE_NAV_VIEW.HomeURL = dct["HomeURL"]
            except NameError:
                pass

        if "NavColor" in dct and dct["NavColor"]:
            try:
                if not cls.BASE_NAV_VIEW.NavColor:
                    cls.BASE_NAV_VIEW.NavColor = dct["NavColor"]
            except NameError:
                pass

        if "SearchURL" in dct and dct["SearchURL"]:
            try:
                if not cls.BASE_NAV_VIEW.SearchURL:
                    cls.BASE_NAV_VIEW.SearchURL = dct["SearchURL"]
            except:
                pass

        if "SearchModels" in dct and dct["SearchModels"]:
            try:
                for model in dct["SearchModels"]:
                    cls.BASE_NAV_VIEW.SearchModels.append(model)
            except (NameError, TypeError):
                try:
                    cls.BASE_NAV_VIEW.SearchModels.append(dct["SearchModels"])
                except (NameError, TypeError):
                    pass


class NavView(SideBarOptions, SearchOptions, NavBarOptions, TitleOptions, BaseNavOptions, TemplateMixin,
              metaclass=TitleViewMetaclass):
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


TitleViewMetaclass.BASE_NAV_VIEW = NavView
