from django.db import models
from django.conf import settings
# Create your models here.


class Food(models.Model):
    user                    = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name                    = models.CharField(max_length=100)
    order                   = models.IntegerField(default=-1)
    iconName                = models.CharField(max_length=100)
    backgroundColorName     = models.CharField(max_length=100)
    iconColorName           = models.CharField(max_length=100)
    userCreated             = models.BooleanField(default=False)
    selected                = models.BooleanField(default=False)

    def __str__(self):
        return self.user.email + " / " + self.name


class Aggravator(models.Model):
    user                    = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name                    = models.CharField(max_length=100)
    order                   = models.IntegerField(default=-1)
    iconName                = models.CharField(max_length=100)
    backgroundColorName     = models.CharField(max_length=100)
    iconColorName           = models.CharField(max_length=100)
    medicalInfo             = models.CharField(max_length=100, blank=True, default="")
    userCreated             = models.BooleanField(default=False)
    selected                = models.BooleanField(default=False)

    def __str__(self):
        return self.user.email + " / " + self.name



class Symptom(models.Model):
    user                    = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name                    = models.CharField(max_length=100)
    order                   = models.IntegerField(default=-1)
    iconName                = models.CharField(max_length=100)
    backgroundColorName     = models.CharField(max_length=100)
    iconColorName           = models.CharField(max_length=100)
    medicalInfo             = models.CharField(max_length=100, blank=True, default="")
    userCreated             = models.BooleanField(default=False)
    selected                = models.BooleanField(default=False)

    def __str__(self):
        return self.user.email + " / " + self.name



class Comorbidity(models.Model):
    user                    = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name                    = models.CharField(max_length=100)
    order                   = models.IntegerField(default=-1)
    iconName                = models.CharField(max_length=100, blank=True, null=True, default='')
    backgroundColorName     = models.CharField(max_length=100)
    iconColorName           = models.CharField(max_length=100)
    userCreated             = models.BooleanField(default=False)
    selected                = models.BooleanField(default=False)

    def __str__(self):
        return self.user.email + " / " + self.name



class DailyMedication(models.Model):
    user                    = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name                    = models.CharField(max_length=100)
    order                   = models.IntegerField(default=-1)
    iconName                = models.CharField(max_length=100)
    backgroundColorName     = models.CharField(max_length=100)
    iconColorName           = models.CharField(max_length=100)
    dosage                  = models.IntegerField(default=0)
    unit                    = models.CharField(max_length=20, default='mg')    
    startDate               = models.DateField(blank=True, null=True)
    endDate                 = models.DateField(blank=True, null=True)
    present                 = models.BooleanField(default=False)
    userCreated             = models.BooleanField(default=False)
    selected                = models.BooleanField(default=False)

    def __str__(self):
        return self.user.email + " / " + self.name


class FlareMedication(models.Model):
    user                    = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name                    = models.CharField(max_length=100)
    order                   = models.IntegerField(default=-1)
    iconName                = models.CharField(max_length=100)
    backgroundColorName     = models.CharField(max_length=100)
    iconColorName           = models.CharField(max_length=100)
    dosage                  = models.IntegerField(default=0)
    unit                    = models.CharField(max_length=20, default='mg')  
    medicalInfo             = models.CharField(max_length=100, blank=True, default="")
    userCreated             = models.BooleanField(default=False)
    selected                = models.BooleanField(default=False)

    def __str__(self):
        return self.user.email + " / " + self.name





