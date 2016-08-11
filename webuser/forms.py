#coding=utf-8

from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django import forms
from django.contrib import auth
from .models import Webuser,Project,Pay
from django.utils.safestring import mark_safe


class HorizontalRadioRenderer(forms.RadioSelect.renderer):      #水平单选框水平样式
    def render(self):
        return mark_safe(u'\n'.join([u'&nbsp;&nbsp;&nbsp;%s\n ' % w for w in self]))


class LoginForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}),
                               max_length=30, required=True, label=u'用户名', error_messages={'required': u'用户名不能为空'})
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}),
                               label=u'密码', error_messages={'required': u'密码不能为空'},
                               required=True)

    # 上面主要是对样式的覆盖，不用其实也行，只不过很多想要的效果会消失，比如自定义的错误提示等

    class Meta:  # 和数据模型关联类ModelForm必要的子类
        model = User
        fields = ['username', 'password']
        exclude = ['last_login', 'date_joined', 'email', 'confirm_password']  # 剔除不要的表项

    def __init__(self, *args, **kwargs):  # 初始化的方法
        super(LoginForm, self).__init__(*args, **kwargs)

    def clean(self):  # 提示账号密码错误的方法，并且清除内容
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        if username and password:
            self.user_cache = auth.authenticate(username=username, password=password)
            if self.user_cache is None:
                self._errors['username'] = self.error_class([u'账号密码不匹配'])
        return self.cleaned_data


class RegisterForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}),
                               max_length=30, required=True, label=u'用户名', error_messages={'required': u'用户名不能为空'})
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}),
                           label=u'密码', error_messages={'required': u'密码不能为空'},
                           required=True)
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}),
                               label=u'确认密码', error_messages={'required': u'密码不能为空'},
                               required=True)
    email = forms.CharField(widget=forms.EmailInput(attrs={'class': 'form-control'}),
                            required=True,
                            label=u'邮箱',error_messages={'required': u'邮箱不能为空'},
                            max_length=75)

    class Meta:  # 和数据模型关联类ModelForm必要的子类
        model = User
        fields = ['username', 'password','confirm_password','email']
        exclude = ['last_login', 'date_joined']  # 剔除不要的表项

    def __init__(self, *args, **kwargs):  # 初始化的方法
        super(RegisterForm, self).__init__(*args, **kwargs)

    def clean(self):   #自带的数据处理方法
        super(RegisterForm, self).clean()
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        if password and password != confirm_password:
            self._errors['password'] = self.error_class([u'密码不匹配'])
        return self.cleaned_data

class ProfileForm(forms.ModelForm):
    position_choice = ((u'0',u'医师'),(u'1',u'主任'),(u'2',u'病人'),(u'3',u'其他'))

    department_choice = (
    (u'0', u'呼吸内科'), (u'1', u'内分泌科'), (u'2', u'神经内科'), (u'3', u'肾内科'), (u'4', u'肝病研究所'), (u'5', u'中医科'), (u'6', u'骨肿瘤科'),(u'6', u'其他'))

    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}),
                               max_length=20, required=True, label=u'姓名', error_messages={'required': u'姓名为必填项'})
    telephone = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}),
                               max_length=20, required=True, label=u'手机号码', error_messages={'required': u'手机号码为必填项'})
    hospital = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}),
                               max_length=20, required=False, label=u'医院')
    position = forms.ChoiceField(label=u'职位', required=False, choices=position_choice)
    department = forms.IntegerField(widget=forms.RadioSelect(choices=department_choice,attrs={'class':'radio-inline'},renderer=HorizontalRadioRenderer),label=u'科室',
                                    error_messages={'required': u'请选择您的科室'})

    abstract = forms.CharField(label=u'简介',required=False,widget=forms.Textarea(attrs={'width':'900px','heigth':'1450px'}))

    class Meta:  # 和数据模型关联类ModelForm必要的子类
        model = Webuser
        fields = ['name', 'telephone', 'hospital', 'position', 'department', 'abstract']

class ProjectForm(forms.ModelForm):
    classify_choice = ((u'肝癌',u'肝癌'),(u'舌像',u'舌像'))
    Oder_id = forms.CharField(label='',required=False)
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}),
                           max_length=50, required=True, label=u'项目名称', error_messages={'required': u'项目名称不能为空'})
    dir = forms.CharField(label=u'请选择想要上传的文件',required=True,error_messages={'required': u'请选择上传文件'})
    classify = forms.ChoiceField(label=u'项目类型', required=True, choices=classify_choice)

    remark = forms.CharField(label=u'备注', required=False,
                             widget=forms.Textarea(attrs={'width': '900px', 'heigth': '1450px'}))

    class Meta:  # 和数据模型关联类ModelForm必要的子类
        model = Project
        fields = ['name', 'classify', 'remark']

class ChangePasswordForm(forms.Form):
    oldpassword=forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}),label=(u"原口令"),
                                max_length=300,required=True,error_messages={'required': u'请输入原始密码'})
    newpassword=forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}),label=(u"新口令"),
                                max_length=300,required=True,error_messages={'required': u'请输入新密码'})
    newpassword1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}), label=(u"新口令"),
                                  max_length=300,required=True,error_messages={'required': u'请再次输入新密码'})