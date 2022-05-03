import django.forms
from django_filters import FilterSet, CharFilter, ModelChoiceFilter # импортируем filterset, чем-то напоминающий знакомые дженерики
from .models import Post, Author, Category
import django_filters


# создаём фильтр
class PostSearch(FilterSet):
    # date = DateFilter(
    #     field_name="date",
    #     lookup_expr="lt",
    #     label="Дата",
    # )
    # date.field.error_messages = {'invalid': 'Введите дату в формате ДД.ММ.ГГГГ. Например 31.12.2020'}
    # date.field.widget.attrs = {'placeholder': 'ДД.ММ.ГГГГ'}
    date = django_filters.DateFilter(
        label = 'Дата',
        lookup_expr = 'lte',
        widget = django.forms.DateInput(attrs = {'type': 'date'})
    )
    # мы хотим чтобы нам выводило имя хотя бы отдалённо похожее на то что запросил пользователь
    title = CharFilter(
        lookup_expr = 'icontains',
        label = 'Название статьи',
    )
    # мы хотим чтобы нам выводило имя из списка
    author = ModelChoiceFilter(
        queryset = Author.objects.all(),
        label = 'Автор',
        empty_label = 'Все авторы',
    )
    # мы хотим чтобы нам выводило категория списком
    category = ModelChoiceFilter(
        queryset=Category.objects.all(),
        label='Категория',
        empty_label='Все категорииё',
    )
    # Здесь в мета классе надо предоставить модель и указать поля, по которым будет фильтроваться
    # (т. е. подбираться) информация о товарах
    class Meta:
        model = Post
        fields = ('date', 'title', 'author', 'category')
