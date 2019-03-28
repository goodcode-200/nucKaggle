from django.db import models
from django.utils import timezone


# Create your models here.
class EmailVerifyRecord(models.Model):
	code = models.CharField("动态生成的更改信息的链接后缀",max_length=25)
	email = models.CharField("邮箱",max_length=30)
	valid_time = models.DateTimeField("验证建立时间",null=False,default=timezone.now) #验证码的建立时间，由此确定有效时间段
	class Meta:
		verbose_name_plural = '给邮箱发链接(忘记密码)所用信息'