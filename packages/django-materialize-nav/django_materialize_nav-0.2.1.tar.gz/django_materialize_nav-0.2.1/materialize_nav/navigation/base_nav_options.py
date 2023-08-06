from dynamicmethod import dynamicmethod


__all__ = ['BaseNavOptions']


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
        context['request'] = FakeDict(user=request.user, path=request.path, get_full_path=request.get_full_path)

        # Notify that the nav context was loaded
        request.nav_context_loaded = True

        return context
