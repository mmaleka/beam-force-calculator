from django.contrib import admin
from .models import SolveBeamCount, RegisterCount, SolutionBeamCount

# Register your models here.


class SolveBeamCounttAdmin(admin.ModelAdmin):
    list_display = ['id', 'ip_address', 'user', 'views_count', 'time_stamp', 'updated_at']
    list_filter = ['time_stamp', 'user']

admin.site.register(SolveBeamCount, SolveBeamCounttAdmin)



class SolutionBeamViewsCountAdmin(admin.ModelAdmin):
    list_display = ['id', 'ip_address', 'user', 'views_count', 'time_stamp', 'updated_at']
    list_filter = ['time_stamp', 'user']

admin.site.register(SolutionBeamCount, SolutionBeamViewsCountAdmin)



class RegisterViewsCountAdmin(admin.ModelAdmin):
    list_display = ['id', 'ip_address', 'views_count', 'time_stamp', 'updated_at']
    list_filter = ['time_stamp']

admin.site.register(RegisterCount, RegisterViewsCountAdmin)
