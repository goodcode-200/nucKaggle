from django.db import models
from kaggle.models import ComQuestion
from account.models import Team

# Create your models here.
class Schedule(models.Model):
	annotation = "请注意赛程时间n天(n>2)"
	race_name = models.CharField("赛程名字")
	start = models.DateField("赛程开始日期")
	end = models.DateField("赛程结束日期")
	def __str__(self):
		return str(self.race_name)
	class Meta:
		verbose_name_plural = '赛程'
		ordering = ['start']

class MaxScore(models.Model):   #对应一个赛程中的一个题目的某个队伍的最高分
	schedule = models.ForeignKey(Schedule)
	comquestion = models.ForeignKey(ComQuestion)
	team = models.ForeignKey(Team)
	max_score = models.FloatField("最高分数",default=0)
	last_score = models.FloatField("最新分数",default=0)
	ma_sc_dat = models.DateField("最高分日期")
	class Meta:
		verbose_name_plural = '对应一个赛程中的一个题目的某个队伍的最高分'
