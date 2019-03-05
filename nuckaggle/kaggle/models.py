from django.db import models
from django.contrib.auth.models import User
from account.models import Team
from django.utils import timezone
# Create your models here.

#题目
class ComQuestion(models.Model):
	title = models.CharField("题目标题",max_length=25)
	content = models.TextField("题目内容",max_length=1500)
	def __str__(self):
		return str(self.title)
	class Meta:
		verbose_name_plural = '竞赛题目'

#队伍提交文件(索引模型)
class SubmitFile(models.Model):
	#file_id 就是默认 的 自增型的主键
	submitfile = models.FileField(upload_to="submit/%Y/%m/%d",default="submit/default.png")
	team = models.ForeignKey(Team)
	comquestion = models.ForeignKey(ComQuestion)
	score = models.FloatField("文件得分",default=0)
	submit_time = models.DateTimeField(auto_now_add=True)
	status = models.BooleanField("系统计算过得分",default=False)
	message = models.CharField("队伍提交文件的反馈信息",default="系统暂未读取",max_length=30)
	class Meta:
		verbose_name_plural = '队伍提交的文件'

#赛题对应数据源文件（索引模型）
class SourceFile(models.Model):
	# file_id is id which has been given
	sourcefile = models.FileField(upload_to="source/",default="source/default.png")
	comquestion = models.ForeignKey(ComQuestion)
	file_called_name = models.CharField("页面显示文件名(文件名+扩展名)",max_length=30)
	class Meta:
		verbose_name_plural = '赛题对应源文件'

class StdAnswer(models.Model):  #标准答案的文件
	stdanswer = models.FileField(upload_to="stdAnswer/",default="stdAnswer/default.png")
	comquestion = models.OneToOneField(ComQuestion)
	class Meta:
		verbose_name_plural = '赛题用于核验分数的正确答案'

class ScoreComq(models.Model): #对应于每道题的分数
	comquestion = models.ForeignKey(ComQuestion)
	team = models.ForeignKey(Team)
	max_score = models.FloatField("最高分",default=0)
	last_score = models.FloatField("最新分数",default=0)
	ma_sc_dat = models.DateField("最高分日期",null=False,default=timezone.now)
