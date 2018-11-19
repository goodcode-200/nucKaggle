from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class UserProfile(models.Model):
    sex_is = (
        ('man', '男'),
        ('woman', '女'),
    )
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    college = models.CharField("学校", max_length=10)
    student_id = models.CharField("学号", max_length=15)
    phone = models.CharField("联系电话", max_length=12)
    sex = models.CharField("性别", max_length=10, choices=sex_is)

    def __str__(self):
        return str(self.user)

    class Meta:
        verbose_name_plural = '个人信息'




