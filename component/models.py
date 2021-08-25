from django.db import models
from django.conf import settings
# Create your models here.



class Food(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    order = models.IntegerField(default=-1)
    iconName = models.CharField(max_length=100)
    backgroundColorName = models.CharField(max_length=100)
    iconColorName = models.CharField(max_length=100)
    userCreated = models.BooleanField(default=False)
    selected = models.BooleanField(default=False)

    def __str__(self):
        return self.user.first_name + " / " + self.name

