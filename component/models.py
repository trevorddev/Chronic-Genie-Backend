from django.db import models
from django.conf import settings
# Create your models here.


class AppSettings(models.Model):
    symptomsMax             = models.IntegerField(default=10)
    symptomsPreMax          = models.IntegerField(default=20)
    flareMedicationsMax     = models.IntegerField(default=10)
    flareMedicationsPreMax  = models.IntegerField(default=20)
    dailyMedicationsMax     = models.IntegerField(default=10)
    dailyMedicationsPreMax  = models.IntegerField(default=20)
    aggravatorsMax          = models.IntegerField(default=10)
    aggravatorsPreMax       = models.IntegerField(default=20)
    comorbiditiesMax        = models.IntegerField(default=10)
    comorbiditiesPreMax     = models.IntegerField(default=20)
    foodsMax                = models.IntegerField(default=10)
    foodsPreMax             = models.IntegerField(default=20)
    consecutiveDaysToFlare  = models.IntegerField(default=3)

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
        return self.user.first_name + " / " + self.name


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
    iconName                = models.CharField(max_length=100)
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
    startDate               = models.DateField(blank=True, null=True, default="")
    endDate                 = models.DateField(blank=True, null=True, default="")
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
    medicalInfo             = models.CharField(max_length=100, blank=True, default="")
    userCreated             = models.BooleanField(default=False)
    selected                = models.BooleanField(default=False)

    def __str__(self):
        return self.user.email + " / " + self.name




# class daily_report(models.Model):
#     user                    = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#     date                    = models.DateField(auto_now=True)
#     rating                  = models.IntegerField(default=0)
#     notes                   = models.CharField(max_length=500)
    

# class daily_report_foods(models.Model):
#     daily_report_fk         = models.ForeignKey(daily_report, on_delete=models.CASCADE)
#     food_fk                 = models.ForeignKey(Food, on_delete=models.CASCADE)



