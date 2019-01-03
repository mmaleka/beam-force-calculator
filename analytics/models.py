from django.conf import settings
from django.db import models

# Create your models here.
class SolveBeamCount(models.Model):
    ip_address = models.CharField(max_length=220, blank=True, null=True)
    user = models.CharField(max_length=150, db_index=True)
    time_stamp = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    views_count = models.IntegerField(default=0)

    def __str__(self):
        return "{}-{}".format(self.user, self.views_count)

    class Meta:
        ordering = ['-time_stamp']



class SolutionBeamCount(models.Model):
    ip_address = models.CharField(max_length=220, blank=True, null=True)
    user = models.CharField(max_length=150, db_index=True)
    time_stamp = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    views_count = models.IntegerField(default=0)

    def __str__(self):
        return "{}-{}".format(self.user, self.views_count)

    class Meta:
        ordering = ['-time_stamp']


class RegisterCount(models.Model):
    ip_address = models.CharField(max_length=220, blank=True, null=True)
    time_stamp = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    views_count = models.IntegerField(default=0)

    def __str__(self):
        return "{}-{}".format(self.ip_address, self.views_count)

    class Meta:
        ordering = ['-time_stamp']
