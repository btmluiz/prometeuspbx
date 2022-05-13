from django.urls import reverse
from django.utils.functional import LazyObject
from django.utils.translation import gettext_lazy as _

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


DEFAULT_MENU_SECTIONS = {
    "dashboard": {"label": _("Dashboard")},
    "pbx": {"label": _("PBX")},
    "settings": {"label": _("Settings")},
    "no_section": {"label": ""},
}


class Menu:
    def __init__(self):
        self._items = {section: [] for section in DEFAULT_MENU_SECTIONS.keys()}

    def register(self, item, section=None, permissions=None):
        if permissions is None:
            permissions = []
        if not isinstance(item, MenuItem):
            raise UIError("Item must be an instance of MenuItem")

        if not section:
            section = "no_section"

        if not self._items.get(section):
            self._items[section] = []

        self._items[section].append({"permissions": permissions, "item": item})

    def items(self, user):
        _items = {}

        for key, value in self._items.items():
            if len(value) > 0:
                menu_items = []

                for item in value:
                    if user.has_perms(item["permissions"]):
                        menu_items.append(item["item"])

                _items[key] = {
                    "label": DEFAULT_MENU_SECTIONS[key]["label"],
                    "items": menu_items,
                }

        return _items


class DefaultMenu(LazyObject):
    def _setup(self):
        self._wrapped = Menu()


menu = DefaultMenu()
