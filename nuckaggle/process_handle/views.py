from django.shortcuts import render
from django.utils import timezone
from account.models import Team
from .models import Schedule,TeamScore

# Create your views here.


#td = timezone.now() - create
#if td.seconds//60 > 9:  #链接10分钟内有效

def score_list(request,schedule_pk):
	context = {}
	if (schedule_pk!='start%'):
		sd = Schedule.objects.get(pk = schedule_pk)
		ts = TeamScore.objects.filter(schedule = sd)
		context["team_score"] = ts
		context["schedule"] = sd
	else:
		sd = Schedule.objects.all()  #获得的是一个列表
		if(sd):
			schedule = sd[0]  #默认打开第一个赛程的榜单
			ts = TeamScore.objects.filter(schedule=schedule)
			context["team_score"] = ts
			context["schedule"] = schedule #当前的榜单的赛程
		#else 不用管了不用传就是空了
	schedule_list = Schedule.objects.all()
	context["schedule_list"] = schedule_list
	#team_list.sort(key = lambda obj:obj.max_score,reverse = True)
	return render(request,'kaggle/score_list.html',context)