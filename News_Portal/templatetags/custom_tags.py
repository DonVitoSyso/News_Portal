from django import template
from datetime import datetime


register = template.Library()  # если мы не зарегистрируем наши фильтры, # то Django никогда не узнает, где именно их искать и фильтры потеряются


@register.simple_tag()
def current_time(format_string='%b %d %Y'):
   return datetime.utcnow().strftime(format_string)

@register.simple_tag(takes_context=True) #сообщаеv Django, что для работы тега требуется передать контекст
def url_replace(context, **kwargs):
   d = context['request'].GET.copy() #скопировать все параметры текущего запроса
   for k, v in kwargs.items():
       d[k] = v #по указанным полям устанавливаем новые значения
   return d.urlencode()