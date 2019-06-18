from django.db import models
from users.models import User
from django.utils import timezone


# Create your models here.

class Question(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="question", null=True)
    title = models.CharField(max_length=200, null=True)
    content = models.TextField(null=True)
    created = models.DateTimeField(default=timezone.now, null=True)
    integral = models.IntegerField(default=0)
    collect_user = models.ManyToManyField(User, related_name="collect_user_question", blank=True)

    class Meta:
        ordering = ("-created",)

    # 返回的是个必填的字段即null=False
    # 返回的即是admin后台管理里面显示的内容
    def __str__(self):
        return self.content


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="answers")
    answertor = models.ForeignKey(User, on_delete=models.CASCADE, related_name="answertor", null=True)
    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return "Comment by {0} on {1}".format(self.answertor.username, self.question)


class Report_Question(models.Model):
    reporter = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reporter_question")
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="reported_question")
    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{0} 举报了 {1}问答，原因是：{2}.时间是：{3}".format(self.reporter.username, self.question.title, self.content,
                                                      self.created)


class Report_Answer(models.Model):
    reporter = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reporter_answer")
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, related_name="reported_answer")
    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{0} 举报了 {1}用户在标题为{2}的问答下的{3}的回答，原因是：{4},时间是{5}".format(self.reporter.username,
                                                                       self.answer.answertor.username,
                                                                       self.answer.question.title, self.answer.content,
                                                                       self.content, self.created)
