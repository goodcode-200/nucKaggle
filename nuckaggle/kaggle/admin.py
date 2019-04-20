from django.contrib import admin
from .models import ComQuestion,SubmitFile,SourceFile,StdAnswer,ScoreComq
# Register your models here.

@admin.register(ComQuestion)
class ComQuestionAdmin(admin.ModelAdmin):
	list_display = ('id','title')

@admin.register(SubmitFile)
class SubmitFileAdmin(admin.ModelAdmin):
	list_display = ('id','schedule','team','comquestion','score','submit_time','status')

@admin.register(SourceFile)
class SourceFileAdmin(admin.ModelAdmin):
	list_display = ('id','schedule','comquestion','file_called_name')

@admin.register(StdAnswer)
class StdAnswerAdmin(admin.ModelAdmin):
	list_display = ('id','schedule','stdanswer','comquestion')

@admin.register(ScoreComq)
class ScoreComqAdmin(admin.ModelAdmin):
	list_display = ('id','schedule','comquestion','team','max_score','last_score','ma_sc_dat')
