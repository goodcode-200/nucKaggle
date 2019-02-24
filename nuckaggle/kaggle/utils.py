from account.models import Team
from .models import ComQuestion,SubmitFile

#create your utils
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