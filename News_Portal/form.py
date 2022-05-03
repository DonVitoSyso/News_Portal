from django.forms import ModelForm, CharField, ModelChoiceField
from .models import Post, User, Author, Category


# Создаём модельную форму
class PostForm(ModelForm):
    # мы хотим чтобы нам выводило категория списком
    # category = ModelChoiceField(
    #     queryset=Category.objects.all(),
    #     empty_label=None,
    # )
    # в класс мета, как обычно, надо написать модель, по которой будет строится форма и нужные нам поля. Мы уже делали что-то похожее с фильтрами.
    class Meta:
        model = Post
        fields = ['title', 'text', 'author', 'category']

# Создаём модельную форму Для Авторов
class AuthorForm(ModelForm):
    class Meta:
        model = User
        fields = '__all__'