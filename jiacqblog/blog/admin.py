from django.contrib import admin
from .models import Post, Category, Tag, Bigcategory, Copyright, Blog_panel, Onemenu, Twomenu


class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'created_time', 'modified_time', 'category', 'copyright', 'author']
    fields = ['title', 'body', 'img_url','excerpt', 'category', 'copyright', 'usr_name', 'copy_url', 'tags']

    def save_model(self, request, obj, form, change):
        obj.author = request.user
        super().save_model(request, obj, form, change)

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'bigcategory']

class OnemenuAdmin(admin.ModelAdmin):
    list_display = ['name', 'url', 'show', 'z_width', 'order_id']

class TwomenuAdmin(admin.ModelAdmin):
    list_display = ['name', 'url', 'onemenu', 'order_id']


admin.site.register(Post, PostAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Tag)
admin.site.register(Bigcategory)
admin.site.register(Copyright)
admin.site.register(Blog_panel)
admin.site.register(Onemenu, OnemenuAdmin)
admin.site.register(Twomenu, TwomenuAdmin)
