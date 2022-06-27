from django import template

register = template.Library()


@register.filter(name='money_format')
def money_format(value):
    rounded_value = round(value, 2)
    value_str = '${:.2f}'.format(value)

    # Chop off .00 if present
    if str(rounded_value).endswith('.00'):
        value_str = '${:,.0f}'.format(value)

    return value_str
