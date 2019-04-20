from django.http import HttpResponseRedirect
from django.shortcuts import render
from account.models import UserProfile,Team,UserCompetition
from .models import ComQuestion,SubmitFile,SourceFile,StdAnswer,ScoreComq
from .forms import UploadFileForm
#from nuckaggle.settings import MEDIA_ROOT
from django.http import FileResponse,Http404
from django.utils.http import urlquote
import os
import time
from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore, register_events, register_job
import csv
from datetime import datetime
from nuckaggle.settings import MEDIA_ROOT
from .utils import judge_what_schedule
from process_handle.models import TeamScore


# Create your views here.
def home(request):
	context = {}
	context['statu'] = 0
	if not (request.user.is_authenticated()):
		context['statu'] = 1
		context['error'] = '(未登录)登录并报名参赛后方能进入比赛页面'
		username = None
		context["username"] = username
		return render(request,'index.html',context)
	user = request.user
	userprofile = UserProfile.objects.filter(user=user)
	if not userprofile:
		context['statu'] = 1
		context['error'] = '(未报名参赛)登录并报名参赛后方能进入比赛页面'
		username = request.user.username
		context["username"] = username
		return render(request,'index.html',context)
	cq = ComQuestion.objects.all()
	context["questions"] = cq
	context["schedule"] = judge_what_schedule() 
	return render(request,'kaggle/home.html',context)

def race_detail(request,cq_id):
	context = {}
	user = request.user
	userprofile = UserProfile.objects.filter(user = user)
	has_team = False
	if userprofile:
		up = userprofile[0]
		usercompetition = UserCompetition.objects.filter(userprofile = up)
		if usercompetition:
			has_team = True
			uc = usercompetition[0]
			team = uc.team
			submitfile = SubmitFile.objects.filter(team = team,comquestion_id = cq_id)
			context["team"] = team
			context["submitfile"] = submitfile
			context["scorecomq_list"] = ScoreComq.objects.filter(team = team,comquestion_id=cq_id)
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
	schedule = judge_what_schedule()
	context["schedule"] = schedule
	context["comquestion"] = cq
	context["has_team"] = has_team
	return render(request,'kaggle/race_detail.html',context)

def upload_file(request,cq_id):	
	context = {}
	context['statu'] = 0
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
				schedule = judge_what_schedule()  #获得当前的赛程
				sf = SubmitFile()
				sf.team = te
				sf.comquestion = comquestion
				sf.submitfile = request.FILES["file"]
				sf.schedule = schedule             #增加上赛题的赛程信息
				sf.save()
				te.sub_num += 1  #提交次数加一
				te.save()
				context["team"] = te
				context["comquestion"] = comquestion

				return render(request,"kaggle/successful.html",context)
			else:
				context['type'] = '文件类型错误'
				context['statu'] = 1
				context['error'] = '请选择正确类型（*.csv）的文件后再提交'
				referer = request.META.get('HTTP_REFERER')
				context["redirect_to"] = referer
				comquestion = ComQuestion.objects.get(pk=cq_id)
				context["comquestion"] = comquestion
				form = UploadFileForm()
				context["form"] = form
				return render(request,'kaggle/upload_file.html',context)
		else:
			context['type'] = '未选择文件'
			context['statu'] = 1
			context['error'] = '请选择文件后再提交'
			referer = request.META.get('HTTP_REFERER')
			context["redirect_to"] = referer
			comquestion = ComQuestion.objects.get(pk=cq_id)
			context["comquestion"] = comquestion
			form = UploadFileForm()
			context["form"] = form
			return render(request,'kaggle/upload_file.html',context)
	else:
		if not team:
			context['type'] = '无提交权限'
			context['message'] = '您并非队长，无权提交结果文件'
			referer = request.META.get('HTTP_REFERER')
			context["redirect_to"] = referer
			return render(request,'account/error.html',context)
		form = UploadFileForm()
		context["form"] = form
		comquestion = ComQuestion.objects.get(pk=cq_id)
		context["comquestion"] = comquestion
		context["schedule"] = judge_what_schedule()
	return render(request, 'kaggle/upload_file.html',context)

def dlsf(request,cq_id):
	context = {}
	try:
		user = request.user
		up = UserProfile.objects.get(user=user)
		uc = UserCompetition.objects.get(userprofile=up)
	except:
		context['type'] = '无下载数据集权限'
		context['message'] = '注册，报名比赛，组队后的队伍成员登录后才有下载数据集权限'
		referer = request.META.get('HTTP_REFERER')
		context["redirect_to"] = referer
		return render(request,'account/error.html',context)
	schedule = judge_what_schedule()     #判断出当前的赛程
	sf = SourceFile.objects.filter(comquestion_id = cq_id,schedule = schedule)
	comquestion = ComQuestion.objects.get(pk = cq_id)
	context["source_list"] = sf
	context["comquestion"] = comquestion
	context["schedule"] = schedule
	return render(request,'kaggle/dlsf.html',context)

def dl_action(request,sour_id):
	context = {}
	try:
		user = request.user
		up = UserProfile.objects.get(user=user)
		uc = UserCompetition.objects.get(userprofile=up)
	except:
		context['type'] = '无下载数据集权限'
		context['message'] = '注册，报名比赛，组队后的队伍成员登录后才有下载数据集权限'
		referer = request.META.get('HTTP_REFERER')
		context["redirect_to"] = referer
		return render(request,'account/error.html',context)
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
	#@register_job(scheduler,'interval',seconds=120)
	#设计为每天的23:30：10执行提交文件的核查分数操作
	@register_job(scheduler, 'cron', day_of_week='mon-sun', hour='23', minute='30', second='10',id='task_time')
	def test_job():
		schedule = judge_what_schedule()    #获得当前时间是属于那个赛程
		print(schedule)
		submit_list = SubmitFile.objects.filter(status = False,schedule=schedule)  #--------当前赛程的提交
		for i  in submit_list:
			cq = i.comquestion
			stdanswer = StdAnswer.objects.filter(comquestion = cq,schedule=schedule)  #--------当前赛程的该题标准答案
			if(stdanswer):  #如果提交的文件对应有标准答案，一般是有的
				stda = stdanswer[0]
				sf = i.submitfile
				csv1_path = os.path.join(MEDIA_ROOT,stda.stdanswer.url.replace("/media/",""))
				csv2_path = os.path.join(MEDIA_ROOT,sf.url.replace("/media/",""))
				csv1 = open(csv1_path,"r") #读取标准答案
				csv2 = open(csv2_path,"r")  #读取提交的答案
				list_dict_reader1 = list(csv.DictReader(csv1))
				list_dict_reader2 = list(csv.DictReader(csv2))
				num = 0
				try:
					for j in range(len(list_dict_reader1)): #以标准答案的长度为准
						if list_dict_reader1[j]["Label"] == list_dict_reader2[j]["Label"]:
							num += 1
					i.message ="正常读取文件"
				except:
					i.message = "系统核算分数时出现问题,请提交正确格式的文件"
				csv1.close()
				csv2.close()
				i.score = (num/len(list_dict_reader1))*10
				i.status = True
				i.save()   #计算出了一个文件的得分
				#找到当前赛程的题目计数的表
				scorecom = ScoreComq.objects.filter(comquestion_id = i.comquestion_id,team_id = i.team_id,schedule_id=i.schedule_id)
				if scorecom:
					sc = scorecom[0]
				else:
					sc = ScoreComq()
					sc.comquestion_id = i.comquestion_id
					sc.team_id = i.team_id
					sc.schedule_id = i.schedule_id
				sc.last_score = i.score
				if(i.score > sc.max_score):
					sc.max_score = i.score
					sc.ma_sc_dat =datetime.now()
				sc.save()
		team = Team.objects.all()  #计算出该赛程一个队伍获得的最高分
		if team:
			for i in team:  #对应一个队伍
				sum = 0
				sc = ScoreComq.objects.filter(team = i,schedule = schedule)
				if sc:
					for j in sc:
						sum += j.max_score
				tescore = TeamScore.objects.filter(team = i,schedule = schedule)
				if tescore:
					teso = tescore[0]
				else:
					teso = TeamScore()
					teso.team = i
					teso.schedule = schedule
				teso.max_sum_score = sum	
				teso.save()
	# 监控任务
	register_events(scheduler)
	# 调度器开始
	scheduler.start()
except Exception as e:
	print(e)
	# 报错则调度器停止执行
	scheduler.shutdown()

