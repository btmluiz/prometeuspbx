from django.urls import reverse
from django.utils.functional import LazyObject

from ui.exception import UIError


class MenuItem:
    def __init__(self, label, reverse_name, icon=None, items=None, has_sub_path=False):
        """
        :param label: str
        :param reverse_name: str
        :param icon: str
        :param items: list[MenuItem]
        """
        self.label = label
        self._reverse_name = reverse_name
        self.icon = icon
        self.items = items
        self.has_sub_path = has_sub_path

    @property
    def reverse_name(self):
        if self._reverse_name:
            return reverse("ui:%s" % self._reverse_name)
        else:
            return None


class MenuGroup:
    def __init__(self, label, items):
        self.label = label
        self.items = items

    @property
    def is_group(self):
        return True


DEFAULT_MENU_SECTIONS = [
    "dashboard",
    "pbx",
    "no_section",
]


class Menu:
    def __init__(self):
        self._items = {section: [] for section in DEFAULT_MENU_SECTIONS}

    def register(self, item, section=None):
        if not isinstance(item, MenuItem):
            raise UIError("Item must be an instance of MenuItem")

        if not section:
            section = "no_section"

        if not self._items.get(section):
            self._items[section] = []

        self._items[section].append(item)

    @property
    def items(self):
        _items = {}

        for key, value in self._items.items():
            if len(value) > 0:
                _items[key] = value

        return _items


class DefaultMenu(LazyObject):
    def _setup(self):
        self._wrapped = Menu()


menu = DefaultMenu()
