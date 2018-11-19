# -*- coding: utf-8 -*-
from django.shortcuts import render, HttpResponseRedirect
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.contrib.auth.models import User
from kaggle.models import UserProfile



# Create your views here.
def home(request):
    context = {}
    if request.user.is_authenticated():
        username = request.user.username
    else:
        username = None
    context["username"] = username
    return render(request,'index.html', context)


def user_login(request):
    context = {}
    if request.method == 'POST':
        get_name = request.POST.get('username').strip()
        get_password = request.POST.get('password')
        user = authenticate(username=get_name, password=get_password)
        if user is not None:
            if user.is_active:
                request.session["username"] = user.username
                login(request,user)
                return HttpResponseRedirect('/')
            else:
                context['message'] = "您的用户已经被限制,请联系工作人员"
        else:
            context['message'] = "用户名或者密码错误"
        context['type']="登录"
        referer = request.META.get('HTTP_REFERER')
        context["redirect_to"] = referer
        return render(request,'error.html',context)
    return render(request,'login.html')


def register(request):
    context={}
    if request.method == 'POST':
        name = request.POST.get('Username').strip()
        u = User.objects.filter(username=name)
        if u:
            context['type'] = '注册'
            context['message'] = '该名字已被使用'
            referer = request.META.get('HTTP_REFERER')
            context["redirect_to"] = referer
            return render(request,'error.html',context)
        password = request.POST.get('password')
        email = request.POST.get('email')
        user = User.objects.create_user(name, email, password)
        user.save()
        profile = UserProfile()
        profile.user = user
        profile.college = request.POST.get('college')
        profile.student_id = request.POST.get('student_id')
        profile.sex = request.POST.get('sex')
        profile.phone = request.POST.get('phone')
        profile.save()
        url = r'/login'
        return HttpResponseRedirect(url)
    return render(request, 'register.html')


def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/')
