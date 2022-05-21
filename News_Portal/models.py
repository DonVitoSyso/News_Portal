from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum

# Класс написан
class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.SmallIntegerField(default=0)

    # Делаем нормальный вывод имени пользователя
    def __str__(self):
        return f'{self.user}'

    def update_rating(self):
        # Cуммарный рейтинг каждой статьи автора умножается на 3
        postR = self.post_set.aggregate(postRating=Sum('rating'))
        pR = 0
        pR += postR.get('postRating')

        # Суммарный рейтинг всех комментариев автора
        comR = self.user.comment_set.aggregate(commentRating=Sum('rating'))
        cR = 0
        cR += comR.get('commentRating')

        # Суммарный рейтинг всех комментариев к статьям автора
        # compostR = self.user.post_set.aggregate(commentpostRating=Sum('rating'))
        # cpR = 0
        # cpR += compostR.get('commentpostRating')

        self.rating = pR * 3 + cR #+ cpR
        self.save()

# Класс написан
class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    subscribers = models.ManyToManyField(User, )
    # параметр не мой (эталон)
    # subscribers = models.ManyToManyField(User, through='CatSub', blank=True)
    def __str__(self):
        return f'{self.name}'
    # метод не мой (эталон)
    def subscribe(self):
        pass
    # метод не мой (эталон)
    def get_category(self):
        return self.name

# Готов класс
class Post(models.Model):
    title = models.CharField(max_length=255)
    text = models.TextField()
    rating = models.SmallIntegerField(default=0)
    NEWS = 'NW'
    ARTICLE = 'AR'
    CAT_CHOICES = (
        (NEWS, 'Новость'),
        (ARTICLE, 'Статья'),
    )
    type = models.CharField(max_length=2, choices=CAT_CHOICES, default=ARTICLE)
    date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)

    category = models.ManyToManyField(Category, through='PostCategory')
    # из эталона
    isUpdated = models.BooleanField(default=False)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        return f'{self.text[0:125]}...'
    # из эталона
    def email_preview(self):
        return f'{self.text[0:50]}...'

    def get_absolute_url(self):  # добавим абсолютный путь, чтобы после создания нас перебрасывало на страницу с новостью
        return f'/news/{self.id}'
    # из эталона
    def get_cat(self):
        return self.type

    def __str__(self):
        return f'{self.date.date()} :: {self.author} :: {self.title} {self.type}'

# Класс написан
class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    # из эталона
    def __str__(self):
        return f'{self.category} -> {self.post}'

# Класс написан
class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    time = models.DateTimeField(auto_now_add=True)
    rating = models.SmallIntegerField(default=0)

    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()
    # из эталона
    def __str__(self):
        try:
            return self.post.author.user
        except:
            return self.user.username

# из эталона добавляется еще один класс (зачем?)
class CatSub(models.Model):
    category = models.ForeignKey(Category, on_delete = models.CASCADE, blank=True, null=True)
    subscriber = models.ForeignKey(User, on_delete = models.CASCADE, blank=True, null=True)

    def get_user(self):
      return self.subscriber

    def get_category(self):
      return self.category.name

    def get_cat(self):
      return self.category

    def __str__(self):
        return f'{self.subscriber} - {self.category.name}'