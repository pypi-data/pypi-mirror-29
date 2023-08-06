import copy
from django.http import JsonResponse
from django.urls import reverse
from dynamicmethod import dynamicmethod

from .forms import SearchForm

from ..navigation.base_nav_options import BaseNavOptions


__all__ = ["SearchOptions"]


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
