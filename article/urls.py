from django.urls import path
from django.conf.urls import url
from . import views

app_name = 'article'  # 一定要写这一行，否则html中会报错 'article' is not a registered namespace

urlpatterns = [
    path(r'article_post/', views.article_post, name='article_post'),
    path(r'article_list/', views.article_list, name='article_list'),
    path(r'article_detail/<int:id>/', views.article_detail, name='article_detail'),
    path(r'like_article/', views.like_article, name='like_article'),
    path(r'article_search/', views.article_search, name='article_search'),
    path(r'article_myblog/', views.article_myblog, name='article_myblog'),
    path(r'article_mysearch/', views.article_mysearch, name='article_mysearch'),
    path(r'article_delete/<int:id>/', views.article_delete, name='article_delete'),
    path(r'article_collect/<int:id>/', views.article_collect, name='article_collect'),
    path(r'article_collect_cancel/<int:id>/', views.article_collect_cancel, name='article_collect_cancel'),
    path(r'article_change/<int:id>/', views.article_change, name='article_change'),
    path(r'article_othersblog/<int:id>/', views.article_othersblog, name='article_othersblog'),
    path(r'article_othersearch/<int:id>/', views.article_othersearch, name='article_othersearch'),
    path(r'article_report/<int:id>/', views.article_report, name='article_report'),
    path(r'comment_report/<int:id>/', views.comment_report, name='comment_report'),
]
