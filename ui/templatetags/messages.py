from django import template
from django.contrib.messages import constants

register = template.Library()


MESSAGE_CLASS = {
    constants.SUCCESS: "bg-success text-white",
    constants.ERROR: "bg-danger text-white",
    constants.WARNING: "bg-warning text-dark",
}

MESSAGE_ICON = {
    constants.SUCCESS: "check-circle",
    constants.ERROR: "alert-circle",
    constants.WARNING: "alert-triangle",
}


@register.simple_tag(takes_context=False)
def message_classes(message):
    if message.level in MESSAGE_CLASS:
        return MESSAGE_CLASS[message.level]
    else:
        return "bg-primary text-white"


@register.simple_tag(takes_context=False)
def message_icon(message):
    if message.level in MESSAGE_ICON:
        return MESSAGE_ICON[message.level]
    else:
        return "bg-primary text-white"
