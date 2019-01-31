from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class File(models.Model):
    file_id = models.CharField("文件ID", primary_key=True, max_length=20)
    submitter_id = models.CharField("提交人ID", max_length=20)
    status = models.BooleanField()
    file_score = models.FloatField()

    def __str__(self):
        return str(self.file_id)


class TeamSubmit(models.Model):
    file_id = models.CharField("文件ID", max_length=20)
    team_id = models.CharField("队伍ID", max_length=20)


class TeamComposition(models.Model):
    student_id = models.CharField("学号", max_length=9)
    team_id = models.CharField("队伍ID",  max_length=20)




