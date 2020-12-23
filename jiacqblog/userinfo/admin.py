from django.contrib import admin

from .models import UserIP, IP_comment, IP_reply




class UserIPAdmin(admin.ModelAdmin):
    list_display = ['ip', 'address', 'name', 'email', 'first_time', 'last_time', 'views']
    fields = ['ip', 'address', 'name','email']

class IP_commentAdmin(admin.ModelAdmin):
    list_display = ['ip', 'like_comment', 'like_time']

class IP_replyAdmin(admin.ModelAdmin):
    list_display = ['ip', 'like_reply', 'like_time']


admin.site.register(UserIP, UserIPAdmin)
admin.site.register(IP_comment, IP_commentAdmin)
admin.site.register(IP_reply, IP_replyAdmin)