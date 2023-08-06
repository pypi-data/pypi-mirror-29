import collections
import copy
from django.urls import reverse
from django.views.generic.base import TemplateView

from dynamicmethod import dynamicmethod

from .utils import NavHeader, NavItem
from .base_nav_options import BaseNavOptions


__all__ = ['NavHeader', 'NavItem', 'BaseNavOptions', 'TitleOptions', 'NavBarOptions', 'SideBarOptions']


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


class SideBarOptions(BaseNavOptions):
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
