from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def url_active(context, item):
    request = context["request"]
    current_path = request.path
    if current_path == item.reverse_name or (
        item.has_sub_path and current_path.startswith(item.reverse_name)
    ):
        return " active"
    else:
        return ""
