#from account.models import Team
#from .models import ComQuestion,SubmitFile
from process_handle.models import Schedule
from django.utils import timezone

#create your utils
'''
def handle_uploaded_file(f,cq_id,team_id):
	team = Team.objects.get(pk=team_id)
	comquestion = ComQuestion.objects.get(pk=cq_id)
	sf = SubmitFile()
	sf.team = team
	sf.comquestion = comquestion
	sf.save()
	with open('{{MEDIA_ROOT}}/submit_file/{{sf.id}}.txt', 'wb+') as destination:
		for chunk in f.chunks():
			destination.write(chunk)
'''
def judge_what_schedule():   #判断当前时间是处于什么比赛进程   
	sc_list = Schedule.objects.all()
	for i in sc_list:
		if (i.start-timezone.now()).days<0 and (timezone.now()-i.end).days<0:
			return i    #返回了当前的赛程
