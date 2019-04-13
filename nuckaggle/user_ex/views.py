from django.http import HttpResponseRedirect
from django.shortcuts import render
from .forms import IdentifyForm,ResetForm
from .utils import send_forget_email
from django.contrib.auth.models import User
from .models import EmailVerifyRecord
from django.utils import timezone

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
				is_send = send_forget_email(email)
				if is_send:
					return render(request,'user_ex/send_successful.html')
				else:
					return render(request,'user_ex/send_fail.html')
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
	context = {}
	record=EmailVerifyRecord.objects.filter(email = email,code = active_code)
	if record:
		i = record[len(record)-1] #虽然概率极低，有多个的话，取最新的那个（最可能有效）
		create = i.valid_time
		td = timezone.now() - create
		if td.seconds//60 > 9:  #链接10分钟内有效
			context['type'] = '链接超时'
			context['message'] = '此链接已经超时失效，请重新获取'
			referer = request.META.get('HTTP_REFERER')
			context["redirect_to"] = referer
			return render(request,'account/error.html',context)
		email=i.email
		user = User.objects.get(email = email)
		return render(request,'user_ex/pass_reset.html',{'email':email,'username':user.username})
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
