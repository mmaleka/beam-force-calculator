from django.contrib import admin
from .models import Beamlength, BeamSupport, PointLoad, MomentLoad, DistributedLoad


class BeamSupportInline(admin.TabularInline):
    model = BeamSupport
    list_display = ['id', 'beamLength']


class PointLoadInline(admin.TabularInline):
    model = PointLoad
    list_display = ['id', 'beamLength']


class MomentLoadInline(admin.TabularInline):
    model = MomentLoad
    list_display = ['id', 'beamLength']


class DistributedLoadInline(admin.TabularInline):
    model = DistributedLoad
    list_display = ['id', 'beamLength']


class BeamLengthAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'created_at', 'updated_at']
    list_filter = ['user', 'created_at', 'updated_at']
    inlines = [BeamSupportInline, PointLoadInline, MomentLoadInline, DistributedLoadInline]

admin.site.register(Beamlength, BeamLengthAdmin)
