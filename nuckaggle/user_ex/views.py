from django.shortcuts import render
from .forms import IdentifyForm

# Create your views here.
def home(request):
	return render(request,'account/error.html')

def identify(request):
	context = {}
	identify_from = IdentifyForm()
	if request.method == 'POST':
		form = IdentifyForm(request.POST)
		if form.is_valid():
			print("33333333333333")
			email=request.POST.get('email','')
			send_register_email(email,'forget')
			return render(request,'user_ex/send_success.html')
		else:
			print("22222222222")
			context["identify_from"] = identify_from
			return render(request,'user_ex/identify.html',context)
	else:
		print("11111111111111111111")
		context["identify_from"] = identify_from
		return render(request,'user_ex/identify.html',context)