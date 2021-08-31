from django.db import models
from django.conf import settings

from component.models import Food, Symptom, Aggravator, Comorbidity, DailyMedication, FlareMedication
# Create your models here.


class daily_report(models.Model):
    user                    = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date                    = models.DateField()
    rating                  = models.IntegerField(default=0)
    notes                   = models.CharField(max_length=500, blank=True, null=True, default="")
    
    def __str__(self):
        return self.user.email + " / " + str(self.date)


class daily_report_food(models.Model):
    daily_report_id         = models.ForeignKey(daily_report, on_delete=models.CASCADE)
    food_id                 = models.ForeignKey(Food, on_delete=models.CASCADE)


    def __str__(self):
        return self.daily_report_id.user.email + " / " + str(self.daily_report_id.date) + " / " + self.food_id.name


class daily_report_aggravator(models.Model):
    daily_report_id         = models.ForeignKey(daily_report, on_delete=models.CASCADE)
    aggravator_id           = models.ForeignKey(Aggravator, on_delete=models.CASCADE)


    def __str__(self):
        return self.daily_report_id.user.email + " / " + str(self.daily_report_id.date) + " / " + self.aggravator_id.name


class daily_report_symptom(models.Model):
    daily_report_id         = models.ForeignKey(daily_report, on_delete=models.CASCADE)
    symptom_id              = models.ForeignKey(Symptom, on_delete=models.CASCADE)


    def __str__(self):
        return self.daily_report_id.user.email + " / " + str(self.daily_report_id.date) + " / " + self.symptom_id.name


class daily_report_comorbidity(models.Model):
    daily_report_id         = models.ForeignKey(daily_report, on_delete=models.CASCADE)
    comorbidity_id              = models.ForeignKey(Comorbidity, on_delete=models.CASCADE)


    def __str__(self):
        return self.daily_report_id.user.email + " / " + str(self.daily_report_id.date) + " / " + self.comorbidity_id.name


class daily_report_flare_medication(models.Model):
    daily_report_id         = models.ForeignKey(daily_report, on_delete=models.CASCADE)
    flare_medication_id     = models.ForeignKey(FlareMedication, on_delete=models.CASCADE)
    pills                   = models.IntegerField(default=0)

    def __str__(self):
        return self.daily_report_id.user.email + " / " + str(self.daily_report_id.date) + " / " + self.flare_medication_id.name