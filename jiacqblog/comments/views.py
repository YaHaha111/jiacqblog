from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.views.decorators.http import require_POST

from .models import Comment, Reply
from blog.models import Post
from django.contrib import messages
from userinfo.views import update_userinfo, save_comment, save_reply

@require_POST
def comment(request, post_pk):
    # 存入评论用户名和邮箱
    update_userinfo(request)

    post = get_object_or_404(Post, pk=post_pk)
    if request.POST:
        Comment.objects.create(
            name=request.POST['usr'],
            email=request.POST['email'],
            text=request.POST['comment'],
            post=post,
        )

    return redirect(post)


@require_POST
def reply(request, reply_pk):
    # 存入评论用户名和邮箱
    update_userinfo(request)

    reply_again = get_object_or_404(Reply, pk=1)
    reply = get_object_or_404(Comment, pk=reply_pk)
    post = get_object_or_404(Post, pk=reply.post.pk)
    if request.POST:
        Reply.objects.create(
            name=request.POST['usr'],
            email=request.POST['email'],
            text=request.POST['comment'],
            rep_com=reply,
            reply_again=reply_again,
        )
    return redirect(post)


@require_POST
def reply_again(request, reply_again_pk):
    reply_again = get_object_or_404(Reply, pk=reply_again_pk)
    reply = get_object_or_404(Comment, pk=reply_again.rep_com.pk)
    post = get_object_or_404(Post, pk=reply.post.pk)
    if request.POST:
        Reply.objects.create(
            name=request.POST['usr'],
            email=request.POST['email'],
            text=request.POST['comment'],
            rep_com=reply,
            reply_again=reply_again,
        )
    return redirect(post)


def praise(request, comment_pk):
    """好评"""
    com = Comment.objects.get(id=comment_pk)

    like_comment = get_object_or_404(Comment, pk=comment_pk)
    mesg = save_comment(request, like_comment, com)

    good_count = com.good_count
    data = {'good_count': good_count, 'mesg': mesg}
    return JsonResponse(data)

def praiserep(request, reply_pk):
    """好评"""
    reply = Reply.objects.get(id=reply_pk)

    like_reply = get_object_or_404(Reply, pk=reply_pk)
    mesg = save_reply(request, like_reply, reply)

    good_count = reply.good_count
    data = {'good_count': good_count, 'mesg': mesg}
    return JsonResponse(data)


