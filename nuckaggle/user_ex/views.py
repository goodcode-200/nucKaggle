from django.http import HttpResponseRedirect
from django.shortcuts import render
from .forms import IdentifyForm,ResetForm
from .utils import send_forget_email
from django.contrib.auth.models import User
from .models import EmailVerifyRecord

# Create your views here.
def home(request):
	return render(request,'account/error.html')

def identify(request):
	context = {}
	identify_from = IdentifyForm()
	if request.method == 'POST':
		form = IdentifyForm(request.POST)
		if form.is_valid():
			email=request.POST.get('email','')
			us = User.objects.filter(email = email)
			if us:
				send_forget_email(email)
				return render(request,'user_ex/send_successful.html')
			else:
				context["identify_from"] = identify_from
				context["statu"] = 1
				context["error"] = "此邮箱未注册" 
				return render(request,'user_ex/identify.html',context)
		else:
			context["identify_from"] = identify_from
			context["statu"] = 1
			context["error"] = "验证码错误" 
			return render(request,'user_ex/identify.html',context)
	else:
		context["identify_from"] = identify_from
		context["statu"] = 0
		return render(request,'user_ex/identify.html',context)

def reset_password(request,email,active_code):
	record=EmailVerifyRecord.objects.filter(email = email,code = active_code)
	if record:
		for i in record:
			email=i.email
			return render(request,'user_ex/pass_reset.html',{'email':email})
	return HttpResponseRedirect('/')

def modify(request):
	reset_form=ResetForm(request.POST)
	if reset_form.is_valid():
		pwd1=request.POST.get('newpwd1','')
		pwd2=request.POST.get('newpwd2','')
		email=request.POST.get('email','')
		if pwd1!=pwd2:
			return render(request,'user_ex/pass_reset.html',{'msg':'密码不一致！','statu':1,'error':"密码不合规，此页面失效，请重新使用邮箱链接"})
		else:
			user=User.objects.get(email=email)
			user.set_password(pwd2)
			user.save()
			return render(request,'user_ex/reset_success.html')
	else:
		email=request.POST.get('email','')
		return render(request,'user_ex/pass_reset.html',{'msg':reset_form.errors,'statu':1,'error':"密码不合规，此页面失效，请重新使用邮箱链接"})
