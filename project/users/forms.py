# 自定义表单验证
from django import forms
from django.core.validators import RegexValidator

# 注册表单验证
from users.models import Users, Shipaddress


class Reg_in(forms.Form):
    # 验证手机号
    tel = forms.CharField(max_length=11,
                          validators=[
                              RegexValidator(r'^1[3-9]\d{9}','手机号码输入不合法')
                          ])
    # 验证密码
    password = forms.CharField(max_length=20,min_length=6)
    re_password = forms.CharField(max_length=20,min_length=6)

    def __str__(self):
        return self.tel

# 登录验证信息
class Log_in(forms.Form):
    # 验证手机号
    tel = forms.CharField(max_length=11,
                          validators=[
                              RegexValidator(r'^1[3-9]\d{9}', '手机号码输入不合法')
                          ])
    # 验证密码
    password =  forms.CharField(max_length=20,min_length=6)

    def __str__(self):
        return self.tel

# 找回密码
class Find_password(forms.Form):
    tel = forms.CharField(max_length=11,
                          validators=[
                              RegexValidator(r'^1[3-9]\d{9}','手机号码不合法'),
                          ])
    password = forms.CharField(max_length=20,min_length=6)
    re_password = forms.CharField(max_length=20,min_length=6)

    def __str__(self):
        return self.tel

# 个人主页的form验证
class PersonModelFrom(forms.ModelForm):
    class Meta:
        model = Users
        fields = ['name','gender','birthday','school','address','hometown']

# 收货地址验证
class Address_get(forms.ModelForm):
    linktel = forms.CharField(max_length=11,
                          validators=[
                              RegexValidator(r'^1[3-9]\d{9}','手机号码不合法'),
                          ])
    class Meta:
        model = Shipaddress
        fields = ['dormitaryarea','tower','detailarea','person','defaults']
