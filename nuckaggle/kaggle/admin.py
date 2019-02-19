from django.contrib import admin
from .models import ComQuestion,SubmitFile,SourceFile
# Register your models here.

@admin.register(ComQuestion)
class ComQuestionAdmin(admin.ModelAdmin):
	list_display = ('id','title')

@admin.register(SubmitFile)
class SubmitFileAdmin(admin.ModelAdmin):
	list_display = ('id','team','comquestion','score','submit_time','status')

@admin.register(SourceFile)
class SourceFileAdmin(admin.ModelAdmin):
	list_display = ('id','comquestion','file_called_name')
