from django.contrib.auth.models import User, Group
from django.views.generic.edit import CreateView
from .models import BaseRegisterForm
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from News_Portal.models import Author


class BaseRegisterView(CreateView):
    model = User
    form_class = BaseRegisterForm
    success_url = '/'


@login_required
def upgrade_me(request):
    user = request.user
    author_group = Group.objects.get(name='authors')
    print(request.user.groups.name)
    if not request.user.groups.filter(name='authors').exists():
        # мой код
        # user1 = Author(user=user) #сохраняем нашего пользователя в список авторов модели
        # user1.save()
        # код из FAQ
        Author.objects.create(user=user)
        author_group.user_set.add(user)
    else:
        Author.objects.filter(user=user).delete()
        author_group.user_set.remove(user)
    return redirect('/')
