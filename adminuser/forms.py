#coding=utf-8

from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django import forms
from django.contrib import auth
from webuser.models import Webuser,Project,Pay
from django.utils.safestring import mark_safe


#为管理员修改密码设置的表，不用考虑用户原有的密码
class AdminChangePassword(forms.Form):
    newpassword = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}), label=(u"新口令"),
                                  max_length=300, required=True, error_messages={'required': u'请输入新密码'})
    newpassword1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}), label=(u"新口令"),
                               max_length=300, required=True, error_messages={'required': u'请再次输入新密码'})

class ChangePayForm(forms.Form):
    position_choice = ((u'0', u'已支付'), (u'1', u'未支付'))
    pay_status = forms.ChoiceField(label=u'支付状态', required=False, choices=position_choice)
    price = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}),label=u'价格',required=False,max_length=10)