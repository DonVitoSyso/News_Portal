from django import template
from datetime import datetime

register = template.Library()  # если мы не зарегистрируем наши фильтры, # то Django никогда не узнает, где именно их искать и фильтры потеряются
# список слов, которые будем цензурировать
STRONG_WORDS = ["php", "редиска"]


@register.filter() # регистрируем наш фильтр под именем Censor, чтоб django понимал, что это именно фильтр, а не простая функция
def Censor(value): # первый аргумент здесь это то значение, к которому надо применить фильтр, второй аргумент — это аргумент фильтра, т. е. примерно следующее будет в шаблоне value|Censor
   if not isinstance(value, str):
       raise ValueError('Нельзя цензурировать не строку')

   for word in STRONG_WORDS:
       value = value.replace(word[1:], '*' * (len(word)-1))

   return value
