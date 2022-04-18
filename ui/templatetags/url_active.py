from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def url_active(context, viewname):
    request = context["request"]
    current_path = request.path
    if current_path == viewname:
        return " active"
    else:
        return ""
