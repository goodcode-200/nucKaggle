from django.db import models
from django.utils import timezone
from account.models import Team

# Create your models here.
class Schedule(models.Model):
	annotation = models.CharField("注释",max_length=25,default="请注意避免赛程时间冲突")
	#主键
	race_name = models.CharField("赛程名字",max_length=25,primary_key=True)
	start = models.DateTimeField("赛程开始日期",default=timezone.now)
	end = models.DateTimeField("赛程结束时间",default=timezone.now)
	def __str__(self):
		return str(self.race_name)
	class Meta:
		verbose_name_plural = '赛程'
		ordering = ['start']

class TeamScore(models.Model):
	schedule = models.ForeignKey(Schedule)
	team = models.ForeignKey(Team)
	max_sum_score = models.IntegerField("最高总分",default=0)
	class Meta:
		verbose_name_plural = "一个赛程某个队伍的最高总分(用于创建榜单)"