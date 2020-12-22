from django.db.models import Q
from django.shortcuts import get_object_or_404
from .models import UserIP, IP_comment, IP_reply
import json, requests


# 获取用户ip
def get_ip(request):
    try:
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]  # 所以这里是真实的ip
        else:
            ip = request.META.get('REMOTE_ADDR')  # 这里获得代理ip
        return ip
    except:
        ip = None
        return ip


# 存入用户ip或统计用户浏览网站次数
def save_ip(request):
    try:
        ip = get_ip(request)
        if ip is None:
            print('ip is None !(userinfo/views.py/save_ip)')
        else:
            userIP = UserIP
            if userIP.objects.filter(ip__contains=ip).count() != 0:
                userip = get_object_or_404(userIP, ip=ip)
                userip.increase_views()
                print('访问+1！(userinfo/views.py/save_ip)')
            else:
                url = 'http://api.tianapi.com/txapi/ipquery/index?key=%s=%s' % ('7015b947819e8ec42e162ca72acde095&ip', ip)
                req = requests.get(url, timeout=10).text
                content = json.loads(req)
                c = content['newslist'][0]
                userIP.objects.create(
                    ip=ip,
                    address=c,
                )
                print('保存成功！(userinfo/views.py/save_ip)')
    except:
        print('错误！(userinfo/views.py/save_ip)')


# 存入和更新评论的 name + email
def update_userinfo(request):
    try:
        ip = get_ip(request)

        if ip is None:
            print('ip is None !')
        else:
            userip = get_object_or_404(UserIP, ip=ip)
            userip.increase_nameORemail(request.POST['usr'], request.POST['email'])
            print('存入昵称邮箱成功！')
    except:
        print('存入昵称邮箱错误！')


def save_comment(request, like_comment, com):
    try:
        ip = get_ip(request)

        if ip is None:
            print('ip is None !')
            return '出错啦1！'
        else:
            userip = get_object_or_404(UserIP, ip=ip)

            if IP_comment.objects.filter(Q(ip=userip) & Q(like_comment=like_comment)).count() == 0:
                IP_comment.objects.create(
                    ip=userip,
                    like_comment=like_comment,
                )
                com.good_count += 1
                com.save()
                return '成功点赞+1'
            else:
                return '这个你已经点过赞啦！'

    except:
        return '出错啦2！'


def save_reply(request, like_reply, reply):
    try:
        ip = get_ip(request)

        if ip is None:
            print('ip is None !')
            return '出错啦1！'
        else:
            userip = get_object_or_404(UserIP, ip=ip)

            if IP_reply.objects.filter(Q(ip=userip) & Q(like_reply=like_reply)).count() == 0:
                IP_reply.objects.create(
                    ip=userip,
                    like_reply=like_reply,
                )
                reply.good_count += 1
                reply.save()
                return '成功点赞+1'
            else:
                return '这个你已经点过赞啦！'

    except:
        return '出错啦2！'