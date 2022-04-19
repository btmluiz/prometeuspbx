import importlib
import importlib.util
import inspect

from django.conf import settings
from django.urls import path
from django.utils.functional import LazyObject

from ui.exception import UIError
from ui.menu import menu
from ui.pages.base import UIPageGroup, UIPage


class UIPages:
    def __init__(self):
        self._menu = None
        self._urls = None

    def get_all_ui_pages(self):
        urls = []
        for module in settings.PROMETEUSPBX_CONFIG["modules"]:
            str_module = "%s.ui" % module
            if importlib.util.find_spec(str_module):
                ui_module = importlib.import_module(str_module)
                if ui_module.ui_patterns:
                    for ui_page in ui_module.ui_patterns:
                        if inspect.isclass(ui_page) and issubclass(ui_page, UIPage):
                            urls.append(
                                path(
                                    ui_page.path,
                                    ui_page.get_view(),
                                    name=ui_page.path_name,
                                )
                            )
                            if ui_page.is_menu():
                                menu.register(
                                    ui_page.as_menu_item(), ui_page.menu_section
                                )
                        elif isinstance(ui_page.__class__, UIPageGroup):
                            urls = urls + ui_page.get_urls()
                            if ui_page.is_menu():
                                menu.register(ui_page.as_menu_item())
                        else:
                            raise UIError(
                                "all elements of ui_patterns must be an instance of UIPage or UIPageGroup '%s' given"
                                % ui_page
                            )

        self._urls = urls

    @property
    def urls(self):
        if not self._urls:
            self.get_all_ui_pages()
        return self._urls


class LazyUIPages(LazyObject):
    def _setup(self):
        uipages = UIPages()
        self._wrapped = uipages


ui_patterns = LazyUIPages()
