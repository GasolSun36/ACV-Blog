from django.contrib.auth.forms import UserCreationForm
from .models import User
from django import forms


class RegisterForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "email")
        '''
        此外 fields 用于指定表单的字段，这些指定的字段在模板中会被渲染成表单控件
        （即一些 <input> 等表单控件）。 UserCreationForm 中只指定了 fields = ("username",)，
        即用户名，此外还有两个字段密码和确认密码在 UserCreationForm 的属性中指定。
        所以默认的表单渲染后只有用户名（username）、密码、确认密码三个表单控件。
        我们还希望用户注册时提供邮箱地址，所以在 fields 中增加了 email 字段。
        '''

#
# class UserForm(forms.ModelForm):
#     class Meta:
#         model = User
#         fields = ("email",)


