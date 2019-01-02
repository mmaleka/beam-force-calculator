from django.db import models
from django.conf import settings
from django.contrib.contenttypes.models import ContentType

# Create your models here.



class Beamlength(models.Model): # BeamLength
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=5)
    beam_length = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('user', )
        index_together = (('id', 'user'),)

    def __str__(self):
        return 'Project: {}'.format(self.id)

    @property
    def get_content_type(self):
        beam_length = self
        content_type=ContentType.objects.get_for_model(beam_length.__class__)
        return content_type


class BeamSupport(models.Model):
    beamLength = models.ForeignKey(Beamlength, related_name='beam_support', on_delete=models.CASCADE, default=1)
    ROLLER_SUPPORT = 'ROLLER SUPPORT'
    PIN_SUPPORT = 'PIN SUPPORT'
    FIXED_SUPPORT = 'FIXED SUPPORT'
    FREE_SUPPORT = 'FREE SUPPORT'
    SUPPORT_CHOICES = (
        (ROLLER_SUPPORT, 'ROLLER SUPPORT'),
        (PIN_SUPPORT, 'PIN SUPPORT'),
        (FIXED_SUPPORT, 'FIXED SUPPORT'),
        (FREE_SUPPORT, 'FREE SUPPORT')

    )
    support = models.CharField(max_length=20, choices=SUPPORT_CHOICES, default=PIN_SUPPORT)
    support_distance = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.support


class PointLoad(models.Model):
    beamLength = models.ForeignKey(Beamlength, related_name='point_load', on_delete=models.CASCADE, default=1)
    point_load = models.FloatField()
    point_load_distance = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return 'Point Load: {}'.format(self.point_load)


class MomentLoad(models.Model):
    beamLength = models.ForeignKey(Beamlength, related_name='moment_load', on_delete=models.CASCADE, default=1)
    moment_load = models.FloatField()
    moment_load_distance = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return 'Moment Load: {}'.format(self.moment_load)

class DistributedLoad(models.Model):
    beamLength = models.ForeignKey(Beamlength, related_name='distributed_load', on_delete=models.CASCADE, default=1)
    start_distributed_load = models.FloatField()
    end_distributed_load = models.FloatField()
    start_distributed_load_location = models.FloatField()
    end_distributed_load_location = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return 'Distributed Load: {}'.format(self.start_distributed_load)
