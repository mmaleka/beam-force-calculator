from django.contrib import admin
from .models import Comment


class CommentAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'timestamp']

    list_filter = ['user', 'timestamp']


admin.site.register(Comment, CommentAdmin)
