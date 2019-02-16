from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.
class Team(models.Model):
    #team_id = id  使用模型自带的主键值，该值可以自增，自己创建，建议作为队伍的唯一标识
    team_name = models.CharField("队名", max_length=20)

    captain = models.OneToOneField(User)   #一对一关系，一个队伍只有一个队长
    peo_num = models.IntegerField("人数",default=1)
    sub_num = models.IntegerField("提交次数",default=0)
    max_score = models.IntegerField("最高分",default=0)
    last_score = models.IntegerField("最新分数",default=0)
    ma_sc_dat = models.DateField("最高分日期",null=False,default=timezone.now)

    def __str__(self):
        return str(self.team_name)
    class Meta:
        ordering = ['-max_score']
        verbose_name_plural = '队伍'


class UserProfile(models.Model):    #报名比赛后此类对象创建
    #id..作为主键
    sex_is = (
        ('man', '男'),
        ('woman', '女'),
    )
    student_id = models.CharField("学号", max_length=15)
    name = models.CharField("姓名",max_length=10)
    user = models.OneToOneField(User)  #账号，密码，邮箱
    college = models.CharField("学校", max_length=10)

    phone = models.CharField("联系电话", max_length=11)
    sex = models.CharField("性别", max_length=10, choices=sex_is)

    def __str__(self):
        return str(self.user)

    class Meta:
        verbose_name_plural = '个人信息'

class UserCompetition(models.Model):        #最终个人报名比赛信息，添加了队伍关联
    userprofile = models.OneToOneField(UserProfile)
    team = models.ForeignKey(Team)   #一对多关系，写在多的一端
    class Meta:
        verbose_name_plural = '最终报名比赛个人信息'

class TeamRequest(models.Model):             #存放队伍邀请信息并使用
    team = models.ForeignKey(Team)   #一对多关系，写在多的一端
    userprofile = models.ForeignKey(UserProfile)  #一对多关系，写在多的一端
    tag = models.BooleanField("是否由队伍发出")
    class Meta:
        verbose_name_plural = '组队请求'

class Confirm(models.Model):    #修改个人信息时用于身份验证
    confirm_or_not = models.BooleanField("是否验证过身份",default=False)
    user = models.ForeignKey(User)
