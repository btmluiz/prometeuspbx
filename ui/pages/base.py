import abc

from django.urls import path
from django.utils.decorators import classonlymethod

from ui.exception import UIError
from ui.menu import MenuItem

UIPAGE_REQUIRED_ATTRS = ("path", "view")


class UIMenuMixin:
    menu_label = None
    menu_icon = None
    menu_section = None

    @property
    def is_menu(self):
        return bool(self.menu_label)

    @classonlymethod
    def as_menu_item(cls):
        pass


class UIPage(UIMenuMixin):
    path = None
    view = None
    path_name = None

    def __int__(self):
        for attr in UIPAGE_REQUIRED_ATTRS:
            if not getattr(self, attr):
                raise UIError("Field '%s' cannot be null" % attr)

    @classonlymethod
    def get_view(cls):
        from django.views import View

        if callable(cls.view):
            return cls.view
        elif issubclass(cls.view, View):
            return cls.view.as_view()

    @classonlymethod
    def as_menu_item(cls):
        return MenuItem(cls.menu_label, cls.path_name, cls.menu_icon)


class UIPageGroup(UIMenuMixin):
    def __init__(
        self,
        base_path=None,
        group_name=None,
        pages=None,
        menu_label=None,
        menu_icon=None,
    ):
        self._base_path = base_path
        self._group_name = group_name
        self.pages = pages  # type: list[UIPage]
        self.menu_label = menu_label
        self.menu_icon = menu_icon
        if pages is None:
            self.pages = list()  # type: list[UIPage]

    @property
    @abc.abstractmethod
    def base_path(self):
        return self._base_path

    @base_path.setter
    def base_path(self, value):
        self._base_path = value

    @property
    @abc.abstractmethod
    def group_name(self):
        return self._group_name

    @group_name.setter
    def group_name(self, value):
        self._group_name = value

    def add_page(self, page):
        if not isinstance(page, UIPage):
            raise UIError("page must be an instance of UIPage")

        self.pages.append(page)

    def get_urls(self):
        urlpatterns = []
        for page in self.pages:
            p = path(page.path, page.get_view, name=page.path_name)
            urlpatterns.append(p)

        return urlpatterns

    @classonlymethod
    def as_menu_item(cls):
        return MenuItem(
            cls.menu_label,
            None,
            cls.menu_icon,
            [item.as_menu_item() for item in cls.pages],
        )
