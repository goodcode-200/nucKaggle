from django.contrib import admin
from .models import UserProfile,Team,TeamRequest,UserCompetition


# Register your models here.
@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('id','student_id', 'name','user', 'sex', 'phone', 'college')

@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
	list_display = ('id','team_name','captain','peo_num','sub_num','max_score','last_score','ma_sc_dat')  

@admin.register(UserCompetition)
class UserCompetitionAdmin(admin.ModelAdmin):
	list_display =('id','team','userprofile') 

@admin.register(TeamRequest)
class TeamRequestAdmin(admin.ModelAdmin):
	list_display = ('id','team','userprofile','tag')