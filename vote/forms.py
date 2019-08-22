import re
import hashlib
from django import forms
from django.forms import ValidationError
from .models import User

USERNAME_PATTERN = re.compile(r'\w{4,20}')

# \w	匹配字母数字及下划线
# re{ n, m}	匹配 n 到 m 次由前面的正则表达式定义的片段，贪婪方式
# a| b	匹配a或b


"""
# 上面，我们定义了一个与User模型绑定的表单（继承自ModelForm），
# 我们排除了用户编号（no）和注册日期（regdate）这两个属性，
# 并添加了一个repassword属性用来接收从用户表单传给服务器的确认密码。
# 我们在定义User模型时已经对用户名的最大长度进行了限制，
# 上面我们又对确认密码的最小和最大长度进行了限制，
# 但是这些都不足以完成我们对用户输入的验证。
# 上面以`clean_`打头的方法就是我们自定义的验证规则。
# 很明显，`clean_username`是对用户名的检查，
# 而`clean_password`是对密码的检查。
# 由于数据库二维表中不应该保存密码的原文，
# 所以对密码做了一个简单的MD5摘要处理，
# 实际开发中如果只做出这样的处理还不太够，
# 因为即便使用了摘要，仍然有利用彩虹表反向查询破解用户密码的风险，
# 如何做得更好我们会在后续的内容中讲到。为字符串生成MD5摘要的代码如下所示。
"""


def to_md5_hex(message):
    return hashlib.md5(message.encode()).hexdigest()


class RegisterForm(forms.ModelForm):
    repassword = forms.CharField(min_length=8, max_length=20)

    def clean_username(self):
        username = self.cleaned_data['username']
        if not USERNAME_PATTERN.fullmatch(username):
            raise ValidationError('用户名由字母、数字和下划线构成且长度为4-20个字符')
        return username

    def clean_password(self):
        password = self.cleaned_data['password']
        print(password)
        if len(password) < 8 or len(password) > 20:
            raise ValidationError('无效的密码，密码长度为8-20个字符')
        return to_md5_hex(self.cleaned_data['password'])

    def clean_repassword(self):
        repassword = to_md5_hex(self.cleaned_data['repassword'])
        if repassword != self.cleaned_data['password']:  # 这里cleaned password
            #  已经变成了md5
            raise ValidationError('密码和确认密码不一致')

        return repassword

    class Meta:
        model = User
        exclude = ('no', 'regdate')


class LoginForm(forms.Form):
    username = forms.CharField(min_length=4, max_length=20)
    password = forms.CharField(min_length=8, max_length=20)
    captcha = forms.CharField(min_length=4, max_length=4)

    def clean_username(self):
        username = self.cleaned_data['username']
        if not USERNAME_PATTERN.fullmatch(username):
            raise ValidationError('无效的用户名')
        return username

    def clean_password(self):
        return to_md5_hex(self.cleaned_data['password'])


class UserForm(forms.ModelForm):
    password = forms.CharField(min_length=8, max_length=20,
                               widget=forms.PasswordInput, label='密码')

    def clean_username(self):
        username = self.cleaned_data['username']
        if not USERNAME_PATTERN.fullmatch(username):
            raise ValidationError('用户名由字母、数字和下划线构成且长度为4-20个字符')
        return username

    def clean_password(self):
        password = self.cleaned_data['password']
        return password

    class Meta:
        model = User
        exclude = ('no',)
