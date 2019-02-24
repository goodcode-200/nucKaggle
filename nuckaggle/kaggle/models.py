from django.db import models
from django.contrib.auth.models import User
from account.models import Team
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
	score = models.IntegerField("文件得分",default=0)
	submit_time = models.DateTimeField(auto_now_add=True)
	status = models.BooleanField("系统计算过得分",default=False)
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
