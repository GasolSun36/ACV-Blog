from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    # blank=True  让用户在注册时无需填写昵称
    email = models.EmailField(unique=True)
    nickname = models.CharField(max_length=50, blank=True)
    school = models.CharField(max_length=100, blank=True)
    profession = models.CharField(max_length=100, blank=True)
    address = models.CharField(max_length=100, blank=True)
    aboutme = models.TextField(blank=True, default="这个人很懒，什么都没有留下")
    photo = models.FileField(upload_to='images', blank=True)

    class Meta(AbstractUser.Meta):
        pass


class Follow(models.Model):
    follow = models.ForeignKey(User, related_name="follow_user", on_delete=models.CASCADE)  # 被关注者，即博主
    fan = models.ForeignKey(User, related_name="fan_user", on_delete=models.CASCADE)  # 关注者，即粉丝

    def __str__(self):
        return "follow:{0},fan:{1}".format(self.follow, self.fan)


