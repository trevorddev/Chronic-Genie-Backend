from django.db import models

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
    name                    = models.CharField(max_length=100)
    order                   = models.IntegerField(default=-1)
    iconName                = models.CharField(max_length=100)
    backgroundColorName     = models.CharField(max_length=100)
    iconColorName           = models.CharField(max_length=100)
    enabled                 = models.BooleanField(default=False)
    selected                = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Aggravator(models.Model):
    name                    = models.CharField(max_length=100)
    order                   = models.IntegerField(default=-1)
    iconName                = models.CharField(max_length=100)
    backgroundColorName     = models.CharField(max_length=100)
    iconColorName           = models.CharField(max_length=100)
    medicalInfo             = models.CharField(max_length=1000, blank=True, default="")
    selected                = models.BooleanField(default=False)
    enabled                 = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Symptom(models.Model):
    name                    = models.CharField(max_length=100)
    order                   = models.IntegerField(default=-1)
    iconName                = models.CharField(max_length=100)
    backgroundColorName     = models.CharField(max_length=100)
    iconColorName           = models.CharField(max_length=100)
    medicalInfo             = models.CharField(max_length=1000, blank=True, default="")
    selected                = models.BooleanField(default=False)
    enabled                 = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Comorbidity(models.Model):
    name                    = models.CharField(max_length=100)
    order                   = models.IntegerField(default=-1)
    iconName                = models.CharField(max_length=100)
    backgroundColorName     = models.CharField(max_length=100)
    iconColorName           = models.CharField(max_length=100)
    selected                = models.BooleanField(default=False)
    enabled                 = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class DailyMedication(models.Model):
    name                    = models.CharField(max_length=100)
    order                   = models.IntegerField(default=-1)
    iconName                = models.CharField(max_length=100)
    backgroundColorName     = models.CharField(max_length=100)
    iconColorName           = models.CharField(max_length=100)
    dosage                  = models.FloatField(default=0)
    selected                = models.BooleanField(default=False)
    enabled                 = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class FlareMedication(models.Model):
    name                    = models.CharField(max_length=100)
    order                   = models.IntegerField(default=-1)
    iconName                = models.CharField(max_length=100)
    backgroundColorName     = models.CharField(max_length=100)
    iconColorName           = models.CharField(max_length=100)
    dosage                  = models.FloatField(default=0)
    medicalInfo             = models.CharField(max_length=1000, blank=True, default="")
    selected                = models.BooleanField(default=False)
    enabled                 = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class MarketingEmail(models.Model):
    email 					= models.EmailField(verbose_name="email", max_length=60, unique=True)
    is_subscribed           = models.BooleanField(default=True)

    def __str__(self):
        return self.email