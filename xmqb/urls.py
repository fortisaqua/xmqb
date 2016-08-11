"""xmqb URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
# -*- coding: UTF-8 -*-

from django.conf.urls import url
from django.contrib import admin
from webuser.views import index, weblogin,register,profile,project,delete_project,pay,create_project,uploadify_script,profile_delte,Change_Passwords,Change_project
from django.contrib.auth.views import logout
from adminuser import views as admin_views
urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^weblogin/$', weblogin, name='weblogin'),
    url(r'^register/$', register, name='register'),
    url(r'^admin', admin.site.urls),
    url(r'^person/$', profile, name='profile'),
    url(r'^project/$', project, name='project'),
    url(r'^delete_project/$', delete_project, name='delete_project'),
    url(r'^create_project/$', create_project, name='create_project'),
    url(r'^pay/$', pay, name='pay'),
    url(r'^logout/$', logout, {'next_page': '/'}, name='logout'),
    # Here is a method of using url : url( r'...',method_name,arguments_or_just_one_argument_in_this_method_interface,name=.....)
    # So this kind of usage is similar with method like $post('url_in_this_file',{....:.....,.....:......}) in jquery
    # Seems like in django , if you want to transmit arguments to a method , you do not have to add strings like '...../&...='+''+.....
    # This just cost too much time , so just use a dictionary to match argument
    url(r'^uploadify_script/$', uploadify_script, name='upload_script'),
    url(r'^delete_uploadfile/$', profile_delte, name='profile_delte'),
    url(r'^change_passwords/$',Change_Passwords,name='change_passwords'),
    url(r'^change_project/$',Change_project,name='change_project'),
    url(r'^admin_people/$',admin_views.super_profile,name='admin_people'),
    url(r'^user_manage/$',admin_views.users,name='admin_people'),
    url(r'^delete_user/$',admin_views.delete_user,name='delete_user'),
    url(r'^person_change/$',admin_views.change_user,name='person_chagne'),
    url(r'^super_pay_manage/$',admin_views.pay,name='super_pay_manage'),

    # Function changing any user password , changing pay status and delete deal for admin user
    url(r'^super_change_password/$',admin_views.Super_Change_Passwords,name='super_change_password'),
    url(r'^super_change_pay/$',admin_views.Super_Change_pay,name='super_change_pay'),
    url(r'^deleat_pay/$',admin_views.deal_delete,name='delete_pay'),

]
