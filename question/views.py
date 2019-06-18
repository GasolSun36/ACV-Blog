from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Question, Answer, Report_Question,Report_Answer
from users.models import User
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.db.models import Q


# Create your views here.

def question_list(request):
    questions = Question.objects.all()
    return render(request, 'question/question_list.html', {'questions': questions})


@login_required(login_url='/users/login/')
def question_post(request):
    user = User.objects.get(username=request.user.username)
    if request.method == "POST":
        content = request.POST.get('content', None)
        integral = request.POST.get('integral', None)
        title = request.POST.get('title', None)
        # article_id = request.POST.get('article_id', None)
        new_question = Question()
        new_question.content = content
        new_question.author = user
        new_question.title = title
        new_question.integral = integral
        new_question.save()
        return redirect('question:question_list')
    else:
        pass
    return render(request, 'question/question_post.html')


@login_required(login_url='/users/login/')
def question_detail(request, id):
    question = Question.objects.get(id=id)
    user = User.objects.get(username=request.user.username)
    a = Question.objects.filter(id=id, collect_user=user)
    if request.method == "POST":
        pass
        content = request.POST.get('content', None)
        new_answer = Answer()
        new_answer.question = question
        new_answer.content = content
        new_answer.answertor = user
        new_answer.save()
    else:
        pass
    return render(request, 'question/question_detail.html', {'question': question, 'user': user, 'a': a})


def question_search(request):
    search = request.GET.get('search', None)
    error_msg = ''
    if search:
        questions = Question.objects.filter(Q(title__icontains=search) | Q(content__icontains=search))
    else:
        # 将 search 参数重置为空,否则search则为None
        search = ''
        questions = Question.objects.all()
    return render(request, 'question/question_search.html', {'questions': questions})


@login_required(login_url='/users/login/')
def question_myquestion(request):
    user = User.objects.get(username=request.user.username)
    questions = Question.objects.filter(author=user)
    return render(request, 'question/question_myquestion.html', {'questions': questions})


@login_required(login_url='/users/login/')
def question_mysearch(request):
    search = request.GET.get('search', None)
    user = User.objects.get(username=request.user.username)
    error_msg = ''
    if search:
        questions = Question.objects.filter((Q(title__icontains=search) | Q(content__icontains=search)), author=user)
    else:
        # 将 search 参数重置为空,否则search则为None
        search = ''
        questions = Question.objects.filter(author=user)
    return render(request, 'question/question_mysearch.html', {'questions': questions})


@login_required(login_url='/users/login/')
def question_delete(request, id):
    # 根据 id 获取需要删除的文章
    question = Question.objects.get(id=id)
    # 调用.delete()方法删除文章
    question.delete()
    # 完成删除后返回文章列表
    return redirect("question:question_list")


@login_required(login_url='/users/login/')
@csrf_exempt
def question_change(request, id):
    user = User.objects.get(username=request.user.username)
    question = Question.objects.get(id=id)
    if request.method == "POST":
        title = request.POST.get('title', None)
        content = request.POST.get('content', None)
        integral = request.POST.get('integral', None)
        question.title = title
        question.content = content
        question.integral = integral
        question.save()
        return redirect('question:question_detail', id)
    else:
        return render(request, "question/question_change.html", {"question": question})


def question_othersquestion(request, id):
    user = User.objects.get(id=id)
    questions = Question.objects.filter(author=user)
    return render(request, 'question/question_othersquestion.html', {'questions': questions, 'user': user})


def question_othersearch(request, id):
    search = request.GET.get('search', None)
    user = User.objects.get(id=id)
    error_msg = ''
    if search:
        questions = Question.objects.filter((Q(title__icontains=search) | Q(content__icontains=search)), author=user)
    else:
        # 将 search 参数重置为空,否则search则为None
        search = ''
        questions = Question.objects.filter(author=user)
    return render(request, 'question/question_othersearch.html', {'questions': questions, 'user': user})


@login_required(login_url='/users/login/')
def question_collect(request, id):
    # 根据 id 获取需要收藏的文章
    question = Question.objects.get(id=id)
    user = User.objects.get(username=request.user.username)
    # 多对多关系赋值时用add而不是=
    question.collect_user.add(user)
    question.save()
    # 完成收藏后返回文章详情
    a = Question.objects.filter(id=id, collect_user=user)
    return render(request, 'question/question_detail.html', {'question': question, 'user': user, 'a': a})


@login_required(login_url='/users/login/')
def question_collect_cancel(request, id):
    # 根据 id 获取需要取消收藏的文章
    question = Question.objects.get(id=id)
    user = User.objects.get(username=request.user.username)
    # 多对多关系消除时用remove而不是赋值为None或者remove（）
    question.collect_user.remove(user)
    question.save()
    a = Question.objects.filter(id=id, collect_user=user)
    # 完成收藏后返回文章详情
    return render(request, 'question/question_detail.html', {'question': question, 'user': user, 'a': a})


@login_required(login_url='/users/login/')
@csrf_exempt
def question_report(request, id):
    user = User.objects.get(username=request.user.username)
    question = Question.objects.get(id=id)
    if request.method == "POST":
        content = request.POST.get('content', None)
        ra = Report_Question()
        ra.reporter = user
        ra.question = question
        ra.content = content
        ra.save()
        return render(request, 'report_success.html')
    else:
        return render(request, 'question/question_report.html', {'question': question})


@login_required(login_url='/users/login/')
@csrf_exempt
def answer_report(request, id):
    # 传进来的id是回答的id
    answer = Answer.objects.get(id=id)
    user = User.objects.get(username=request.user.username)
    if request.method == "POST":
        content = request.POST.get('content', None)
        ra = Report_Answer()
        ra.reporter = user
        ra.answer = answer
        ra.content = content
        ra.save()
        return render(request, 'report_success.html')
    else:
        return render(request, 'question/answer_report.html', {'answer': answer})
