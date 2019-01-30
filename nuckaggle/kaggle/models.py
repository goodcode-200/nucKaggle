from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class UserProfile(models.Model):
    sex_is = (
        ('man', '男'),
        ('woman', '女'),
    )

    person_status_is = (
        ('register', '注册'),
        ('Participant',  '参赛'),
        ('team', '组队'),
    )
    student_id = models.CharField("学号", primary_key=True, max_length=9)
    user = models.OneToOneField(User)
    college = models.CharField("学校", max_length=10)

    phone = models.CharField("联系电话", max_length=11)
    sex = models.CharField("性别", max_length=10, choices=sex_is)
    person_status = models.CharField("个人状态", max_length=10, choices=person_status_is)

    def __str__(self):
        return str(self.user)

    class Meta:
        verbose_name_plural = '个人信息'


class Team(models.Model):
    team_id = models.CharField("队伍ID", primary_key=True, max_length=20)
    team_name = models.CharField("队名", max_length=20)

    captain_id = models.CharField("队长ID", max_length=20)
    number = models.CharField("人数", max_length=20)
    number_of_submissions = models.CharField("提交次数", max_length=20)
    team_score = models.IntegerField()
    userProfile = models.OneToOneField(UserProfile, on_delete=models.CASCADE)  # 建立一对一表

    def __str__(self):
        return str(self.team_name)


class File(models.Model):
    file_status_is = (
        ('form error', '格式不对'),
        ('unsubmitted',  '未提交'),
        ('submitted', '已提交'),
    )
    file_id = models.CharField("文件ID", primary_key=True, max_length=20)
    file_name = models.CharField("文件名", max_length=20)  # new
    submitter_id = models.CharField("提交人ID", max_length=20)
    submitter_team = models.ForeignKey(Team, on_delete=models.CASCADE)
    file_status = models.CharField("文件状态", max_length=10, choices=file_status_is)
    file_score = models.FloatField("得分")

    def __str__(self):
        return str(self.file_id)


class TeamSubmit(models.Model):
    file_id = models.CharField("文件ID", max_length=20)
    team_id = models.CharField("队伍ID", max_length=20)

    def __str__(self):
        return str(self.file_id)


class TeamComposition(models.Model):
    student_id = models.CharField("学号", max_length=9)
    team_id = models.CharField("队伍ID",  max_length=20)

    def __str__(self):
        return str(self.team_id)





