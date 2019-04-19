# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.utils import timezone


# Create your views here.
def home(request):
    context = {}
    if request.user.is_authenticated():
        username = request.user.username
    else:
        username = None
    context["username"] = username
    return render(request,'index.html', context)
