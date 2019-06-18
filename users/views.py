from django.shortcuts import render, redirect, reverse
from .forms import RegisterForm
from .models import User, Follow
from article.models import Article
from question.models import Question
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required


def register(request):
    # 只有当请求为 POST 时，才表示用户提交了注册信息
    redirect_to = request.POST.get('next', request.GET.get('next', ''))
    if request.method == 'POST':
        # request.POST 是一个类字典数据结构，记录了用户提交的注册信息
        # 这里提交的就是用户名（username）、密码（password）、邮箱（email）
        # 用这些数据实例化一个用户注册表单
        form = RegisterForm(request.POST)

        # 验证数据的合法性
        if form.is_valid():
            # 如果提交数据合法，调用表单的 save 方法将用户数据保存到数据库
            form.save()
            if redirect_to:
                # 注册成功，跳转回前一页
                return redirect('login')
            else:
                # 否则跳转回首页
                return redirect('login')
    else:
        # 请求不是 POST，表明用户正在访问注册页面，展示一个空的注册表单给用户
        form = RegisterForm()

    # 渲染模板
    # 如果用户正在访问注册页面，则渲染的是一个空的注册表单
    # 如果用户通过表单提交注册信息，但是数据验证不合法，则渲染的是一个带有错误信息的表单
    return render(request, 'users/register.html', context={'form': form, 'next': redirect_to})


def index(request):
    # 查询所有的文章列表
    articles = Article.objects.all()
    articles_views = Article.objects.all().order_by('-total_views')
    return render(request, 'article_list.html', {'articles': articles, 'articles_views': articles_views})


def user_info(request):
    user = User.objects.get(username=request.user.username)
    return render(request, "users_info.html", {"user": user})


def myself_edit(request):
    # 改数据时先规定各个组件的name，然后使用request.POST.get('name',None),取得对应组件里面的数据
    # None表示如果没有取到东西返回None
    user = User.objects.get(username=request.user.username)
    if request.method == "GET":
        return render(request, "user_info_edit.html", {"user": user})
    else:
        school = request.POST.get('school', None)
        nickname = request.POST.get('nickname', None)
        profession = request.POST.get('profession', None)
        address = request.POST.get('address', None)
        aboutme = request.POST.get('aboutme', None)
        USER = User.objects.get(username=request.user.username)
        USER.school = school
        USER.nickname = nickname
        USER.profession = profession
        USER.address = address
        USER.aboutme = aboutme
        USER.save()
        return render(request, 'users_info.html', {'user': USER})


def my_image(request):
    USER = User.objects.get(username=request.user.username)
    if request.method == 'POST':
        # img = request.POST['img']
        img = request.POST.get('img', None)
        USER.photo = img
        USER.save()
        return HttpResponse("1")
    else:
        return render(request, 'imagecrop.html', {'user': USER})


@login_required(login_url='/users/login/')
def others_info(request, id):
    user = User.objects.get(username=request.user.username)  # 自己
    USER = User.objects.get(id=id)  # 博主
    f = Follow.objects.filter(follow=USER, fan=user)
    # 如果user和USER不一样即打开的博主和自己不一样，user是博主，follow是自己
    if user != USER:
        return render(request, 'others_info.html', {'user': USER, 'follow': user, 'f': f})
    else:
        return render(request, 'users_info.html', {'user': user})


@login_required(login_url='/users/login/')
def follow_on(request, id):
    # 传进来的id是博主的id即被关注者的id
    user = User.objects.get(username=request.user.username)
    USER = User.objects.get(id=id)
    f = Follow()
    f.follow = USER
    f.fan = user
    f.save()
    return render(request, 'others_info.html', {'user': USER, 'follow': user, 'f': f})


@login_required(login_url='/users/login/')
def follow_cancel(request, id):
    # 传进来的id是博主的id即被关注者的id
    user = User.objects.get(username=request.user.username)
    USER = User.objects.get(id=id)
    f = Follow.objects.filter(follow=USER, fan=user)
    f.delete()
    return render(request, 'others_info.html', {'user': USER, 'follow': user, 'f': f})


@login_required(login_url='/users/login/')
def user_follow(request):
    user = User.objects.get(username=request.user.username)
    f = Follow.objects.filter(fan=user)
    return render(request, 'user_follow.html', {'f': f})


@login_required(login_url='/users/login/')
def user_fan(request):
    user = User.objects.get(username=request.user.username)
    f = Follow.objects.filter(follow=user)
    return render(request, 'user_fan.html', {'f': f})


@login_required(login_url='/users/login/')
def my_collect(request):
    user = User.objects.get(username=request.user.username)
    articles = Article.objects.filter(collect_user=user)
    questions = Question.objects.filter(collect_user=user)
    return render(request, 'my_collect.html', {'articles': articles, 'questions': questions})
