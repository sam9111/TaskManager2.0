from django import template

register = template.Library()


@register.filter(name="addclass", is_safe=True)
def addclass(value, arg):
    return value.as_widget(attrs={"class": arg})
