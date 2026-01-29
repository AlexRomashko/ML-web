from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now


class Data(models.Model):
    name = models.TextField()
    N = models.IntegerField()
    K = models.IntegerField()
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE)
    date = models.DateField(default=now)
    linkToFile = models.FileField(upload_to='uploads')

    def __str__(self):
        return self.name


    class Meta:
        ordering: ['+date']

