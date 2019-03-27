from django.shortcuts import render
from .forms import IdentifyForm
from .utils import send_forget_email
from django.contrib.auth.models import User

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

def reset_password(request):