from django.urls import path
from .views import (PostList, PostDetail, PostUpdateView,
                    PostDeleteView, PostCreateView, PostSearchView,
                    UserUpdateView, ArticleCreateView)  # импортируем наше представление

urlpatterns = [
    # path — означает путь. В данном случае путь ко всем товарам у нас останется пустым, позже станет ясно, почему
    path('', PostList.as_view()),
    # т. к. сам по себе это класс, то нам надо представить этот класс в виде view. Для этого вызываем метод as_view
    path('<int:pk>', PostDetail.as_view(), name='news'),  # pk — это первичный ключ товара, который будет выводиться у нас в шаблон
    path('news/<int:pk>/edit', PostUpdateView.as_view(), name='news_update'),
    path('news/<int:pk>/delete', PostDeleteView.as_view(), name='news_delete'),
    path('news/create/', PostCreateView.as_view(), name='news_create'),
    path('articles/<int:pk>/edit', PostUpdateView.as_view(), name='articles_update'),
    path('articles/<int:pk>/delete', PostDeleteView.as_view(), name='articles_delete'),
    path('articles/create/', ArticleCreateView.as_view(), name='articles_create'),
    path('search/', PostSearchView.as_view(), name='news_search'),
    path('user', UserUpdateView.as_view(), name='user_update'),
]
