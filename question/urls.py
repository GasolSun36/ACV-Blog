from django.urls import path
from django.conf.urls import url
from . import views

app_name = 'question'  # 一定要写这一行，否则html中会报错 'article' is not a registered namespace

urlpatterns = [
    path(r'question_post/', views.question_post, name='question_post'),
    path(r'question_list/', views.question_list, name='question_list'),
    path(r'question_detail/<int:id>/', views.question_detail, name='question_detail'),
    path(r'question_search/', views.question_search, name='question_search'),
    path(r'question_myquestion/', views.question_myquestion, name='question_myquestion'),
    path(r'question_mysearch/', views.question_mysearch, name='question_mysearch'),
    path(r'question_delete/<int:id>/', views.question_delete, name='question_delete'),
    path(r'question_change/<int:id>/', views.question_change, name='question_change'),
    path(r'question_othersquestion/<int:id>/', views.question_othersquestion, name='question_othersquestion'),
    path(r'question_othersearch/<int:id>/', views.question_othersearch, name='question_othersearch'),
    path(r'question_collect/<int:id>/', views.question_collect, name='question_collect'),
    path(r'question_collect_cancel/<int:id>/', views.question_collect_cancel, name='question_collect_cancel'),
    path(r'question_report/<int:id>/', views.question_report, name='question_report'),
    path(r'answer_report/<int:id>/', views.answer_report, name='answer_report'),
]
