from django.urls import path

from . import views

app_name = 'comments'
urlpatterns = [
    path('comment/<int:post_pk>', views.comment, name='comment'),
    path('reply/<int:reply_pk>', views.reply, name='reply'),
    path('reply_again/<int:reply_again_pk>', views.reply_again, name='reply_again'),
    path('praise/<int:comment_pk>', views.praise),
    path('praiserep/<int:reply_pk>', views.praiserep),
]