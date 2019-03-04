from django.http import HttpResponseRedirect
from django.shortcuts import render
from account.models import UserProfile,Team
from .models import ComQuestion,SubmitFile,SourceFile
from .forms import UploadFileForm
#from nuckaggle.settings import MEDIA_ROOT
from django.http import FileResponse,Http404
from django.utils.http import urlquote
import os
import time
from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore, register_events, register_job


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

def upload_file(request,cq_id):	
	context = {}
	user = request.user
	team = Team.objects.filter(captain=user)
	if request.method == 'POST':
		form = UploadFileForm(request.POST,request.FILES)
		if form.is_valid():
			name = request.FILES["file"].name
			index = name.index('.')
			exte = name[index+1::]
			if exte=="csv":   #只接受*.csv文件的上传，否则就页面拦截
				te = team[0]
				comquestion = ComQuestion.objects.get(pk=cq_id)
				sf = SubmitFile()
				sf.team = te
				sf.comquestion = comquestion
				sf.submitfile = request.FILES["file"]
				sf.save()
				te.sub_num += 1  #提交次数加一
				te.save()
				context["team"] = te
				return render(request,"kaggle/successful.html",context)
			else:
				context['type'] = '文件类型错误'
				context['message'] = '请选择正确类型（*.csv）的文件后再提交'
				referer = request.META.get('HTTP_REFERER')
				context["redirect_to"] = referer
				return render(request,'account/error.html',context)
		else:
			context['type'] = '未选择文件'
			context['message'] = '请选择文件后再提交'
			referer = request.META.get('HTTP_REFERER')
			context["redirect_to"] = referer
			return render(request,'account/error.html',context)
	else:
		if not team:
			context['type'] = '无提交权限'
			context['message'] = '您并非队长，无权提交结果文件'
			referer = request.META.get('HTTP_REFERER')
			context["redirect_to"] = referer
			return render(request,'account/error.html',context)
		form = UploadFileForm()
		context["form"] = form
	return render(request, 'kaggle/upload_file.html',context)

def dlsf(request,cq_id):
	context = {}
	sf = SourceFile.objects.filter(comquestion_id = cq_id)
	comquestion = ComQuestion.objects.get(pk = cq_id)
	context["source_list"] = sf
	context["comquestion"] = comquestion
	return render(request,'kaggle/dlsf.html',context)

def dl_action(request,sour_id):
	sf = SourceFile.objects.get(pk = sour_id)
	file = sf.sourcefile
	file_name = sf.file_called_name
	try:
		response =FileResponse(file)  
		response['content_type'] = "application/octet-stream"    
		response['Content-Disposition'] = 'attachment;filename=' + urlquote(file_name)  
		return response
	except Exception:
		raise Http404

def about(request):
	return render(request,'kaggle/aboutKaggle.html')


try:  
	# 实例化调度器
	scheduler = BackgroundScheduler()
	# 调度器使用DjangoJobStore()
	scheduler.add_jobstore(DjangoJobStore(), "default")
	# 'cron'方式循环，周一到周五，每天9:30:10执行,id为工作ID作为标记
	# ('scheduler',"interval", seconds=1)  #用interval方式循环，每一秒执行一次
	#@register_job(scheduler,'interval',seconds=4)
	@register_job(scheduler, 'cron', day_of_week='mon-fri', hour='9', minute='30', second='10',id='task_time')
	def test_job():
	   t_now = time.localtime()
	   print(t_now,"\n","测试成功，加油")

	# 监控任务
	register_events(scheduler)
	# 调度器开始
	scheduler.start()
except Exception as e:
	print(e)
	# 报错则调度器停止执行
	scheduler.shutdown()

