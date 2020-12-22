from django.contrib import admin
from .models import Comment, Reply


class CommentAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'url', 'post', 'created_time']
    fields = ['name', 'email', 'url', 'text', 'post']

class ReplyAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'url', 'rep_com', 'created_time', 'reply_again']
    fields = ['name', 'email', 'url', 'text', 'rep_com', 'reply_again']


admin.site.register(Comment, CommentAdmin)
admin.site.register(Reply, ReplyAdmin)