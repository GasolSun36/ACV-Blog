from django.db import models

# Create your models here.

from django.db import models
from users.models import User
from django.utils import timezone
from django.urls import reverse


class Article(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="article", null=True)
    title = models.CharField(max_length=200)
    content = models.TextField(null=True)
    created = models.DateTimeField(default=timezone.now, null=True)
    updated = models.DateTimeField(auto_now=True, null=True)
    users_like = models.ManyToManyField(User, related_name="articles_like", blank=True)
    collect_user = models.ManyToManyField(User, related_name="collect_user", blank=True)
    total_views = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ("-updated",)

    # 对数据库中的这两个字段建立索引，以后就可以通过每篇文章的id和slug来获取该文章对象了，
    # 这样建立索引以后，能提高读取文章对象的速度。
    def __str__(self):
        return self.title


class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name="comments")
    commentator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="commentator", null=True)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return "{0} 在 {1}博客中评论了".format(self.commentator.username, self.article)


class Report_Article(models.Model):
    reporter = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reporter_article")
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name="reported_article")
    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{0} 举报了 {1}博客，原因是：{2}.时间是{3}".format(self.reporter.username, self.article.title, self.content,
                                                     self.created)


class Report_Commit(models.Model):
    reporter = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reporter_commit")
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name="reported_commit")
    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{0} 举报了 {1}用户在标题为{2}的博客下的{3}的评论，原因是：{4}。时间是{5}".format(self.reporter.username,
                                                                       self.comment.commentator.username,
                                                                       self.comment.article.title, self.comment.body,
                                                                       self.content, self.created)
