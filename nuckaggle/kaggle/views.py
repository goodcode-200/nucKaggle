from django.http import HttpResponseRedirect
from django.shortcuts import render
from account.models import UserProfile,Team
from .models import ComQuestion,SubmitFile,SourceFile
from .forms import UploadFileForm
#from nuckaggle.settings import MEDIA_ROOT
from django.http import FileResponse,Http404
from django.utils.http import urlquote
import os


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
			te = team[0]
			comquestion = ComQuestion.objects.get(pk=cq_id)
			sf = SubmitFile()
			sf.team = te
			sf.comquestion = comquestion
			sf.submitfile = request.FILES["file"]
			sf.save()
			context["team"] = te
			return render(request,"kaggle/successful.html",context)
		else:
			context['type'] = '未选择文件或其他'
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
