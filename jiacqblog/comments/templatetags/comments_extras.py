import markdown
from django import template
from django.db.models import Count
from userinfo.models import UserIP
from userinfo.views import get_ip

register = template.Library()


@register.inclusion_tag('comments/inclusions/_form.html', takes_context=True)
def show_comment_form(context, post):
    ip = get_ip(context['request'])
    userIP = UserIP.objects.filter(ip=ip).values('name', 'email')
    return {
        'post': post,
        'userIP': userIP,
    }


@register.inclusion_tag('comments/inclusions/_list.html', takes_context=True)
def show_comments(context, post):
    comment_list = post.comment_set.all().order_by('-created_time').annotate(c=Count('reply'))

    ip = get_ip(context['request'])
    userIP = UserIP.objects.filter(ip=ip).values('name', 'email')

    md = markdown.Markdown(extensions=[
        # 包含 缩写、表格等常用扩展
        'markdown.extensions.extra',
        # 语法高亮扩展
        'markdown.extensions.codehilite',
    ])
    n = 0
    for comment in comment_list:
        comment_list[n].text = md.convert(comment.text)
        n += 1

    comment_count = comment_list.count()
    return {
        'comment_count': comment_count,
        'comment_list': comment_list,
        'userIP': userIP,
    }


@register.inclusion_tag('comments/inclusions/_reply_form.html', takes_context=True)
def show_reply_form(context, comment, userIP):
    userIP = userIP

    return {
        'comment': comment,
        'userIP': userIP,
    }


@register.inclusion_tag('comments/inclusions/_reply_again_form.html', takes_context=True)
def show_reply_again_form(context, reply, userIP):
    userIP = userIP
    return {
        'reply': reply,
        'userIP': userIP
    }


@register.inclusion_tag('comments/inclusions/_reply.html', takes_context=True)
def show_reply_list(context, comment):

    userIP = context['userIP']

    reply_list = comment.reply_set.all().order_by('created_time')
    md = markdown.Markdown(extensions=[
        # 包含 缩写、表格等常用扩展
        'markdown.extensions.extra',
        # 语法高亮扩展
        'markdown.extensions.codehilite'
    ])

    n = 0
    for reply in reply_list:
        reply_list[n].text = md.convert(reply.text)
        # reply_list[n].reply_again = get_object_or_404(Reply, pk=reply_list[n].reply_again)
        n += 1

    return {
        'reply_list': reply_list,
        'userIP': userIP
    }



