from django.shortcuts import render
from .models import ComQuestion
from account.models import UserProfile

# Create your views here.
def home(request):
	context = {}
	if not (request.user.is_authenticated()):
		context['type'] = '未登录'
		context['message'] = '登录并报名参赛后方能进入比赛页面'
		referer = request.META.get('HTTP_REFERER')
		context["redirect_to"] = referer
		return render(request,'account/error.html',context)
	user = request.user
	userprofile = UserProfile.objects.filter(user=user)
	if not userprofile:
		context['type'] = '未报名参赛'
		context['message'] = '登录并报名参赛后方能进入比赛页面'
		referer = request.META.get('HTTP_REFERER')
		context["redirect_to"] = referer
		return render(request,'account/error.html',context)
	cq = ComQuestion.objects.all()
	context["questions"] = cq
	return render(request,'kaggle/home.html',context)

def race_detail(request,cq_id):
	context = {}
	cq = ComQuestion.objects.get(pk=cq_id)
	cq_list = ComQuestion.objects.all()
	for i in cq_list:
		if i.id > int(cq_id):
			context["next_comquestion"] = i
			break
	rev_cq_list = list(reversed(cq_list))
	for i in rev_cq_list:
		if i.id < int(cq_id):
			context["previous_comquestion"] = i
			break
	context["comquestion"] = cq
	return render(request,'kaggle/race_detail.html',context)
