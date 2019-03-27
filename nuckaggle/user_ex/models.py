from django.db import models

# Create your models here.
class EmailVerifyRecord(models.Model):
	type_is = (
		('register','注册'),
		('forget', '忘记密码'),
	)
	code = models.CharField("动态生成的更改信息的链接后缀",max_length=25)
	email = models.CharField("邮箱",max_length=30)
	class Meta:
		verbose_name_plural = '给邮箱发链接(忘记密码)所用信息'