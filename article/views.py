from django.shortcuts import render, redirect, get_object_or_404, reverse
from .forms import ArticlePostForm, CommentForm
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .models import Article, Comment, Report_Article, Report_Commit
from django.views.decorators.http import require_POST
from django.utils import timezone
from users.models import User
from django.db.models import Q


def article_list(request):
    articles = Article.objects.all()
    articles_views = Article.objects.all().order_by('-total_views')
    return render(request, 'article_list.html', {'articles': articles, 'articles_views': articles_views})


@login_required(login_url='/users/login/')
@csrf_exempt
def article_post(request):
    user = User.objects.get(username=request.user.username)
    if request.method == "POST":
        article_post_form = ArticlePostForm(request.POST)
        if article_post_form.is_valid():
            # cd = article_post_form.cleaned_data
            try:
                new_article = Article()
                # new_article=Article.objects.create_article(title,content)
                # new_article = article_post_form.save(commit=False)
                author = user
                new_article.author = author
                title = request.POST.get('title', None)
                content = request.POST.get('content', None)
                new_article.title = title
                new_article.content = content
                new_article.save()
                return redirect('article:article_list')
            except:
                return HttpResponse("2")
    else:
        article_post_form = ArticlePostForm()

        return render(request, "article/article.html",
                      {"article_post_form": article_post_form})


@login_required(login_url='/users/login/')
def article_detail(request, id):
    article = Article.objects.get(id=id)
    user = User.objects.get(username=request.user.username)
    a = Article.objects.filter(id=id, collect_user=user)
    article.total_views += 1
    # 只修改article的total_views属性
    article.save(update_fields=['total_views'])

    if request.method == "POST":
        comment = request.POST.get('comment', None)
        # article_id = request.POST.get('article_id', None)
        new_comment = Comment()
        new_comment.article = article
        new_comment.body = comment
        new_comment.commentator = user
        new_comment.save()
    else:
        pass
    return render(request, 'article/article_detail.html',
                  {'article': article, 'user': user, 'a': a})


@csrf_exempt
@require_POST
@login_required(login_url='/users/login/')
def like_article(request):
    article_id = request.POST.get("id")
    action = request.POST.get("action")
    if article_id and action:
        try:
            article = Article.objects.get(id=article_id)
            if action == "like":
                article.users_like.add(request.user)
                return HttpResponse("1")
            else:
                article.users_like.remove(request.user)
                return HttpResponse("2")
        except:
            return HttpResponse("no")


def article_search(request):
    search = request.GET.get('search', None)
    error_msg = ''
    if search:
        articles = Article.objects.filter(Q(title__icontains=search) | Q(content__icontains=search))
    else:
        # 将 search 参数重置为空,否则search则为None
        search = ''
        articles = Article.objects.all()
    return render(request, 'article/article_search.html', {'articles': articles})


@login_required(login_url='/users/login/')
def article_myblog(request):
    user = User.objects.get(username=request.user.username)
    articles = Article.objects.filter(author=user)
    return render(request, 'article/article_myblog.html', {'articles': articles})


@login_required(login_url='/users/login/')
def article_mysearch(request):
    search = request.GET.get('search', None)
    user = User.objects.get(username=request.user.username)
    error_msg = ''
    if search:
        articles = Article.objects.filter((Q(title__icontains=search) | Q(content__icontains=search)), author=user)
    else:
        # 将 search 参数重置为空,否则search则为None
        search = ''
        articles = Article.objects.filter(author=user)
    return render(request, 'article/article_mysearch.html', {'articles': articles})


@login_required(login_url='/users/login/')
def article_delete(request, id):
    # 根据 id 获取需要删除的文章
    article = Article.objects.get(id=id)
    # 调用.delete()方法删除文章
    article.delete()
    # 完成删除后返回文章列表
    return redirect("article:article_list")


@login_required(login_url='/users/login/')
@csrf_exempt
def article_change(request, id):
    user = User.objects.get(username=request.user.username)
    article = Article.objects.get(id=id)
    if request.method == "POST":
        title = request.POST.get('title', None)
        content = request.POST.get('content', None)
        article.title = title
        article.content = content
        article.save()
        return redirect('article:article_detail', id)
    else:
        return render(request, "article/article_change.html", {"article": article})


def article_othersblog(request, id):
    user = User.objects.get(id=id)
    articles = Article.objects.filter(author=user)
    return render(request, 'article/article_othersblog.html', {'articles': articles, 'user': user})


def article_othersearch(request, id):
    search = request.GET.get('search', None)
    user = User.objects.get(id=id)
    error_msg = ''
    if search:
        articles = Article.objects.filter((Q(title__icontains=search) | Q(content__icontains=search)), author=user)
    else:
        # 将 search 参数重置为空,否则search则为None
        search = ''
        articles = Article.objects.filter(author=user)
    return render(request, 'article/article_othersearch.html', {'articles': articles, 'user': user})


@login_required(login_url='/users/login/')
def article_collect(request, id):
    # 根据 id 获取需要收藏的文章
    article = Article.objects.get(id=id)
    user = User.objects.get(username=request.user.username)
    # 多对多关系赋值时用add而不是=
    article.collect_user.add(user)
    article.save()
    # 完成收藏后返回文章详情
    a = Article.objects.filter(id=id, collect_user=user)
    return render(request, 'article/article_detail.html', {'article': article, 'user': user, 'a': a})


@login_required(login_url='/users/login/')
def article_collect_cancel(request, id):
    # 根据 id 获取需要取消收藏的文章
    article = Article.objects.get(id=id)
    user = User.objects.get(username=request.user.username)
    # 多对多关系消除时用remove而不是赋值为None或者remove（）
    article.collect_user.remove(user)
    article.save()
    a = Article.objects.filter(id=id, collect_user=user)
    # 完成收藏后返回文章详情
    return render(request, 'article/article_detail.html', {'article': article, 'user': user, 'a': a})


@login_required(login_url='/users/login/')
@csrf_exempt
def article_report(request, id):
    user = User.objects.get(username=request.user.username)
    article = Article.objects.get(id=id)
    if request.method == "POST":
        content = request.POST.get('content', None)
        ra = Report_Article()
        ra.reporter = user
        ra.article = article
        ra.content = content
        ra.save()
        return render(request, 'report_success.html')
    else:
        return render(request, 'article/article_report.html', {'article': article})


@login_required(login_url='/users/login/')
@csrf_exempt
def comment_report(request, id):
    # 传进来的id是评论的id
    comment = Comment.objects.get(id=id)
    user = User.objects.get(username=request.user.username)
    if request.method == "POST":
        content = request.POST.get('content', None)
        ra = Report_Commit()
        ra.reporter = user
        ra.comment = comment
        ra.content = content
        ra.save()
        return render(request, 'report_success.html')
    else:
        return render(request, 'article/comment_report.html', {'comment': comment})
