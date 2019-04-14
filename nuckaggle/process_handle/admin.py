from django.contrib import admin
from .models import Schedule,MaxScore

# Register your models here.
@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
	list_display = ('id','race_name','start','end')

@admin.register(MaxScore)
class MaxScoreAdmin(admin.ModelAdmin):
	list_display = ('id','schedule','comquestion','team','max_score')