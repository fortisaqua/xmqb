#-*- coding: UTF-8 -*-
from django.shortcuts import render,redirect
from webuser.forms import LoginForm,RegisterForm,ProfileForm,ProjectForm,ChangePasswordForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib import auth,messages
from webuser.models import Webuser,Project,Pay,UploadFile
from django.utils import timezone
import time
from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect,csrf_exempt
from django.http import HttpResponse,HttpResponseRedirect,JsonResponse
import json
import os
from django.conf import settings
import uuid
from .forms import AdminChangePassword,ChangePayForm
# Create your views here.

# Create your views here.
@csrf_exempt
def super_profile(request):
    if not request.user.is_authenticated():
        return redirect('/weblogin')
    if not request.user.is_superuser:
        return redirect('/person')
    user = request.user
    if request.method == 'GET':
        form = ProfileForm(instance=user, initial={
            'name': user.webuser.name,
            'telephone': user.webuser.telephone,
            'hospital': user.webuser.hospital,
            'position': user.webuser.position,
            'department': user.webuser.department,
            'abstract': user.webuser.abstract
        })
        return render(request, 'adminuser/person_page_info.html', {'form': form})
    else:
        form = ProfileForm(request.POST)
        if form.is_valid():
            webuser = Webuser.objects.get(user=request.user)
            webuser.name = form.cleaned_data.get('name')
            webuser.telephone = form.cleaned_data.get('telephone')
            webuser.hospital = form.cleaned_data.get('hospital')
            webuser.position = form.cleaned_data.get('position')
            webuser.department = form.cleaned_data.get('department')
            webuser.abstract = form.cleaned_data.get('abstract')
            webuser.save()
            messages.add_message(request, messages.SUCCESS, u'您的资料已经编辑成功.')
        return render(request, 'adminuser/person_page_info.html', {'form': form})

@csrf_exempt
def users(request):
    if not request.user.is_authenticated():
        return redirect('/weblogin')
    if not request.user.is_superuser:
        return redirect('/person')
    Users = Webuser.objects.all()
    return render(request, 'adminuser/person_manage.html', {'Users': Users})

@csrf_exempt
def change_user(request):
    Id = request.GET['user_id']
    if not request.user.is_authenticated():
        print 'not log in'
        return redirect('/weblogin')
    elif not request.user.is_superuser:
        print 'not super user'
        return redirect('/')
    if request.method == 'GET':
        thisUser = Webuser.objects.get(user_id=Id)
        form = ProfileForm(initial={
            'name': thisUser.name,
            'telephone': thisUser.telephone,
            'hospital': thisUser.hospital,
            'position': thisUser.position,
            'department': thisUser.department,
            'abstract': thisUser.abstract
        })
        return render(request,'adminuser/person_change.html',{'form':form,'show_id':Id})
    else:
        form = ProfileForm(request.POST)
        if form.is_valid():
            webuser = Webuser.objects.get(user_id=Id)
            webuser.name = form.cleaned_data.get('name')
            webuser.telephone = form.cleaned_data.get('telephone')
            webuser.hospital = form.cleaned_data.get('hospital')
            webuser.position = form.cleaned_data.get('position')
            webuser.department = form.cleaned_data.get('department')
            webuser.abstract = form.cleaned_data.get('abstract')
            webuser.save()
            messages.add_message(request, messages.SUCCESS, u'您的资料已经编辑成功.')
        return render(request, 'adminuser/person_change.html', {'form': form,'show_id':Id})

@csrf_exempt
def delete_user(request):
    if not request.user.is_authenticated():
        return redirect('/weblogin')
    if not request.user.is_superuser:
        return redirect('/person')
    del_user = User.objects.get(pk=request.GET['user_id'])
    # files=UploadFile.objects.filter(Order_ID=del_project.Order_ID)
    # for del_file in files:
    #     file_delete(del_file.directory)
    del_user.delete()
    Users = Webuser.objects.all()
    return render(request, 'adminuser/person_manage.html', {'Users': Users})

def pay(request):
    if not request.user.is_authenticated():
        return redirect('/weblogin')
    if not request.user.is_superuser:
        return redirect('/')
    pay = Pay.objects.all()
    return render(request, 'adminuser/pay_manage.html', {'pay': pay})

# 新增管理员修改用户密码功能
@csrf_exempt
def Super_Change_Passwords(request):
    if not request.user.is_authenticated():
        return redirect('/weblogin')
    if not request.user.is_superuser:
        return redirect('/')
    user_id=request.GET['user_id']
    if request.method == "POST":
        form =AdminChangePassword(request.POST)
        if form.is_valid():
            newpassword = form.cleaned_data['newpassword']
            newpassword1 = form.cleaned_data['newpassword1']
            if not newpassword == newpassword1:
                messages.add_message(request, messages.SUCCESS, u'两次输入不一致!!')
                return render(request, 'adminuser/change_password.html', {'form': form,'userid':user_id})
            else:
                thisUser = User.objects.get(id=user_id)
                thisUser.set_password(newpassword)
                thisUser.save()
                messages.add_message(request, messages.SUCCESS, u'用户密码修改成功!!')
                return render(request, 'adminuser/change_password.html', {'form': form,'userid':user_id})
        else:
            return render(request, 'adminuser/change_password.html', {'form': form,'userid':user_id})
    else:
        form = AdminChangePassword()
        return render(request, 'adminuser/change_password.html', {'form': form,'userid':user_id})

@csrf_exempt
def Super_Change_pay(request):
    Id = request.GET['Order_id']
    if not request.user.is_authenticated():
        return redirect('/weblogin')
    if not request.user.is_superuser:
        return redirect('/')
    if request.method == "POST":
        form = ChangePayForm(request.POST)
        if form.is_valid():
            pay_status = form.cleaned_data['pay_status']
            price = form.cleaned_data['price']
            thisPay = Pay.objects.get(project_id=Id)
            if thisPay:
                thisPay.price = price
                thisPay.is_pay = pay_status
                thisPay.save()
                messages.add_message(request, messages.SUCCESS, u'交易信息修改成功!!')
                return render(request, 'adminuser/pay_change.html', {'form': form, 'Order_id': Id})
            else:
                messages.add_message(request, messages.SUCCESS, u'此交易不存在!!')
                return render(request, 'adminuser/pay_change.html', {'form': form, 'Order_id': Id})
        else:
            return render(request, 'adminuser/pay_change.html', {'form': form, 'Order_id': Id})
    else:
        thisPay = Pay.objects.get(project_id=Id)
        form = ChangePayForm(initial={'pay_status':thisPay.is_pay,
                                      'price':thisPay.price})
        return render(request,'adminuser/pay_change.html',{'form':form,'Order_id':Id})

@csrf_exempt
def deal_delete(request):
    if not request.user.is_authenticated():
        return redirect('/weblogin')
    if not request.user.is_superuser:
        return redirect('/')
    del_deal = Pay.objects.get(project_id=request.GET['Order_id'])
    # files=UploadFile.objects.filter(Order_ID=del_project.Order_ID)
    # for del_file in files:
    #     file_delete(del_file.directory)
    del_deal.delete()
    deals = Pay.objects.all()
    return render(request, 'adminuser/pay_manage.html', {'pay': deals})
