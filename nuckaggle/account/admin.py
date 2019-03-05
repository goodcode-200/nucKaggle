from django.contrib import admin
from .models import UserProfile,Team,TeamRequest,UserCompetition,Confirm


# Register your models here.
@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('id','student_id', 'name','user', 'sex', 'phone', 'college')

@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
	list_display = ('id','team_name','captain','peo_num','sub_num','max_score')  

@admin.register(UserCompetition)
class UserCompetitionAdmin(admin.ModelAdmin):
	list_display =('id','team','userprofile') 

@admin.register(TeamRequest)
class TeamRequestAdmin(admin.ModelAdmin):
	list_display = ('id','team','userprofile','tag')

@admin.register(Confirm)
class ConfirmAdmin(admin.ModelAdmin):
	list_display = ('id','confirm_or_not','user')