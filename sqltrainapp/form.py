from django import forms
from .models import User
from django.core.exceptions import ValidationError
import re

# 登录验证
class login_f(forms.Form):
    user_name = forms.CharField()
    pwd = forms.CharField()

    def clean(self):
        user_name = self.cleaned_data.get('user_name')
        pwd = self.cleaned_data.get('pwd')
        if User.objects.filter(user_name=user_name) and User.objects.get(user_name=user_name).pwd == pwd:
            pass
        else:
            self.add_error("user_name",'用户名或密码错误')
            raise forms.ValidationError('')
        return self.cleaned_data



class register_f(forms.Form):
    user_name = forms.CharField(label='user_name', min_length=4, max_length=15,
                                error_messages={'min_length' or 'max_length': "用户名的长度在4-15个字符内"})
    pwd = forms.CharField(min_length=6, max_length=40, required=True,
                                    error_messages={'min_length' or 'max_length': "密码的长度在6-40个字符内"})
    pwd2 = forms.CharField(min_length=6, max_length=40, required=True,
                                     error_messages={'min_length' or 'max_length': "密码的长度在6-40个字符内"})

    # 从这里分界，上面是基本验证，下面是特殊验证。只有基本验证通过类，才会进行特殊验证。

    # 该类函数是自定义的函数，格式为clean_*，且*必须是字段名（这样才能与字段绑定）这样才会被调用，返回值为user
    def clean_user_name(self):  # 验证用户名是否已经存在
        user_name = self.cleaned_data.get('user_name')
        if User.objects.filter(user_name=user_name):
            raise forms.ValidationError('用户名已存在')
        return user_name

    # def clean_user_password(self):  # 验证两次密码的一致性
    #     user_password = self.cleaned_data.get("user_password")    # 能取得user_password的值
    #     user_password2 = self.cleaned_data.get("user_password2")  # 不能取得user_password2的值，原因可能是该方法与字段绑定
    #     print(user_password,user_password2)
    #     if user_password != user_password2:
    #         raise forms.ValidationError('两次密码不一致')
    #     return user_password

    # 该函数是重写的函数，返回值必须确定为cleaned_data

    # @property
    def clean(self):  # 事实证明，验证两个密码一致，必须在这个函数里，因为只有这个函数能取得所有的值
        pwd = self.cleaned_data.get('pwd')
        pwd2 = self.cleaned_data.get('pwd2')
        if pwd != pwd2:
            self.add_error('pwd', '两次输入密码不匹配')
            # 添加自定义错误，并绑定到 user_password2 (必须绑定在字段上，而不能随意定义一个变量名) 上，可以被error.user_password2调用
            raise forms.ValidationError('')  # 这个也不能少
        return self.cleaned_data  # 注意此处一定要return clean_data,否则会报错
