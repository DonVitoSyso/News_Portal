from django.shortcuts import render
from django.views.generic import UpdateView, ListView, DetailView, CreateView, DeleteView  # импортируем класс получения деталей объекта
# импортируем класс, который говорит нам о том, что в этом представлении мы будем выводить список объектов из БД
from .models import Post, Category
from datetime import datetime

from django.core.paginator import Paginator  # импортируем класс, позволяющий удобно осуществлять постраничный вывод
from .search import PostSearch  # импортируем недавно написанный фильтр
from .form import PostForm, AuthorForm  # импортируем нашу форму

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin


# class PostList(ListView):
#     model = Post  # указываем модель, объекты которой мы будем выводить
#     template_name = 'news.html'  # указываем имя шаблона, в котором будет лежать HTML, в котором будут все инструкции о том, как именно пользователю должны вывестись наши объекты
#     context_object_name = 'news'  # это имя списка, в котором будут лежать все объекты, его надо указать, чтобы обратиться к самому списку объектов через HTML-шаблон
#     queryset = Post.objects.order_by('-id')
#
#     # метод get_context_data нужен нам для того, чтобы мы могли передать переменные в шаблон. В возвращаемом словаре context будут храниться все переменные. Ключи этого словаря и есть переменные, к которым мы сможем потом обратиться через шаблон
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['time_now'] = datetime.utcnow()  # добавим переменную текущей даты time_now
#         context[
#             'value1'] = None  # добавим ещё одну пустую переменную, чтобы на её примере посмотреть работу другого фильтра
#         return context

class PostList(ListView):#(PermissionRequiredMixin, ListView):
    # Проверка на права доступа. Авторизация обязательная!!!
    # permission_required = ('<app>.<action>_<model>', '<app>.<action>_<model>')

    model = Post  # указываем модель, объекты которой мы будем выводить
    template_name = 'news.html'  # указываем имя шаблона, в котором будет лежать HTML, в котором будут все инструкции о том, как именно пользователю должны вывестись наши объекты
    context_object_name = 'news'
    paginate_by = 10  # поставим постраничный вывод в 10 элементов
    ordering = ['-id']
    # queryset = Post.objects.all()  # Default: Model.objects.all()
    # form_class = PostForm  # добавляем форм класс, чтобы получать доступ к форме через метод POST

    # метод get_context_data нужен нам для того, чтобы мы могли передать переменные в шаблон. В возвращаемом словаре context будут храниться все переменные. Ключи этого словаря и есть переменные, к которым мы сможем потом обратиться через шаблон
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = PostSearch(self.request.GET, queryset=self.get_queryset())  # вписываем наш фильтр в контекст
        context['count'] = Post.objects.all().count() #добавили поле для общего колличества страниц
        # context['categories'] = Category.objects.all()
        # context['form'] = PostForm()
        return context


# создаём представление, в котором будут детали конкретного отдельного товара
# дженерик для получения деталей о новости
class PostDetail(DetailView):
    # model = Post  # модель всё та же, но мы хотим получать детали конкретно отдельного товара
    template_name = 'new.html'  # название шаблона будет new.html
    context_object_name = 'new'  # название объекта. в нём будет
    queryset = Post.objects.all()

# дженерик для создания объекта. Надо указать только имя шаблона и класс формы, который мы написали в прошлом юните. Остальное он сделает за вас
class PostCreateView(PermissionRequiredMixin, CreateView):
    # Проверка на права доступа
    model = Post
    permission_required = ('New_Portal.add_new',)
    template_name = 'new_create.html'
    form_class = PostForm
    # success_url = '/news/'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.type = 'NEWS'
        return super().form_valid(form)


# дженерик для редактирования объекта
class PostUpdateView(PermissionRequiredMixin, UpdateView):
    # Проверка на права доступа
    permission_required = ('New_Portal.change_new',)
    template_name = 'new_create.html'
    form_class = PostForm
    # success_url = '/news/'

    # метод get_object мы используем вместо queryset, чтобы получить информацию об объекте, который мы собираемся редактировать
    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)


# дженерик для удаления новостей
class PostDeleteView(PermissionRequiredMixin, DeleteView):
    # Проверка на права доступа
    permission_required = ('New_Portal.delete_new',)
    template_name = 'new_delete.html'
    context_object_name = 'new'
    queryset = Post.objects.all()
    success_url = '/news/'


class PostSearchView(ListView):
    model = Post  # указываем модель, объекты которой мы будем выводить
    template_name = 'new_search.html'  # указываем имя шаблона, в котором будет лежать HTML, в котором будут все инструкции о том, как именно пользователю должны вывестись наши объекты
    context_object_name = 'news'
    paginate_by = 10  # поставим постраничный вывод в 10 элементов
    ordering = ['-id']
    # queryset = Post.objects.all()  # Default: Model.objects.all()
    # form_class = PostForm  # добавляем форм класс, чтобы получать доступ к форме через метод POST

    # Помощь ментора обычный get_context_data из PostList не подойдет
    # пагинатор не верно отображает листы
    def get_filter(self):
        return PostSearch(self.request.GET, queryset=super().get_queryset())

    def get_queryset(self):
        return self.get_filter().qs

    def get_context_data(self, **kwargs):
        return {
            **super().get_context_data(**kwargs),
            'filter': self.get_filter(),
        }


class UserUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'author_update.html'
    form_class = AuthorForm

    def get_object(self, **kwargs):
        return self.request.user


# Дженерики под статьи
class ArticleCreateView(PermissionRequiredMixin, CreateView):
    # Проверка на права доступа
    model = Post
    permission_required = ('New_Portal.add_new',)
    template_name = 'new_create.html'
    form_class = PostForm
