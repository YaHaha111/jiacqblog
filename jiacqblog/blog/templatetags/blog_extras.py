from django import template
from django.db.models import Count, Sum
import pandas as pd
from datetime import datetime
from ..models import Post, Category, Tag, Blog_panel, Bigcategory, Onemenu, Twomenu
from django.shortcuts import get_object_or_404
from django.db.models import Max, Min


register = template.Library()



from django.utils.html import format_html
@register.simple_tag
def circle_page(curr_page, loop_page):
    offset = abs(curr_page - loop_page)
    if offset < 3:
        if curr_page == loop_page :
            page_ele = '<li class="currentState"><a href="?page=%s#tt">%s</a></li>' % (loop_page, loop_page)
        else:
            page_ele = '<li><a href="?page=%s#tt">%s</a></li>' % (loop_page, loop_page)
        return format_html(page_ele)
    else:
        return ''


# 脚部信息
@register.inclusion_tag('blog/inclusions/_footer.html', takes_context=True)
def show_footer(context):
    img_url = Blog_panel.objects.filter(id=1).values('name', 'icp_img')
    return {
        'img_url': img_url,
    }


# 顶部信息
@register.inclusion_tag('blog/inclusions/_head.html', takes_context=True)
def show_head(context):
    img_url = Blog_panel.objects.filter(id=1).values('name', 'icon', 'apple_touch_icon', 'dmk_img', 'h12_img', 'h34_img', 'h56_img')
    return {
        'img_url': img_url,
    }


# 头部水平导航条
@register.inclusion_tag('blog/inclusions/_header.html', takes_context=True)
def show_header(context):
    f_menu = Onemenu.objects.all().order_by('order_id')
    z_menu = Twomenu.objects.all().order_by('order_id')
    img_url = Blog_panel.objects.filter(id=1).values('name', 'icon')
    return {
        'img_url': img_url,
        'f_menu': f_menu,
        'z_menu': z_menu,
    }


# 上下文定义
@register.inclusion_tag('blog/inclusions/_previous_next_post.html', takes_context=True)
def show_previous_next_post(context, pk):
    post_revious_id = pk
    post_next_id = pk
    max_post = Post.objects.all().aggregate(Max('id'))
    min_post = Post.objects.all().aggregate(Min('id'))
    max_id = max_post['id__max']
    min_id = min_post['id__min']
    post_revious = ""
    post_next = ""

    if post_revious_id <= min_id:
        post_revious = get_object_or_404(Post, pk=min_id)
    else:
        for _ in range(0, post_revious_id):
            post_revious_id -= 1
            if Post.objects.filter(id=post_revious_id) :
                post_revious = get_object_or_404(Post, pk=post_revious_id)
                break

    if post_next_id >= max_id:
        post_next = get_object_or_404(Post, pk=max_id)
    else:
        for _ in range(post_next_id, max_id):
            post_next_id += 1
            if Post.objects.filter(id=post_next_id) :
                post_next = get_object_or_404(Post, pk=post_next_id)
                break
    return {
        'post_revious': post_revious,
        'post_next': post_next,
    }


# 信息面板
@register.inclusion_tag('blog/inclusions/_panel.html', takes_context=True)
def show_panel(context):
    img_url = Blog_panel.objects.filter(id=1).values('name', 'blog_photo', 'motto')
    # print(img_url[0]['motto'])
    post_count =  Post.objects.all().count()
    category_count = Category.objects.all().count()
    views_count =  Post.objects.all().aggregate(Sum('views'))
    return {
        'img_url': img_url,
        'post_count': post_count,
        'category_count': category_count,
        'views_count': views_count
    }


# 侧边栏分类菜单
@register.inclusion_tag('blog/inclusions/_categories.html', takes_context=True)
def show_categories(context):
    return {
        'category_list': Category.objects.all().annotate(c=Count('post')).filter(c__gt=0), # 去除小于1的
        'bigcategory_list': Bigcategory.objects.all().annotate(c=Count('category')).filter(c__gt=0),
    }


# 侧边栏最新文章
@register.inclusion_tag('blog/inclusions/_recent_posts.html', takes_context=True)
def show_recent_posts(context, num=5):
    recent_post_list = Post.objects.all().order_by('-created_time')[:num]

    return {
        'recent_post_list': recent_post_list,
    }


# 侧边栏日期归档
@register.inclusion_tag('blog/inclusions/_archives.html', takes_context=True)
def show_archives(context):
    date_query1 = Post.objects.values('created_time').order_by('-created_time').annotate(c=Count('content_int'))
    data = {"one": {}, "two": {}}
    df=pd.DataFrame(data)
    for i in range(len(date_query1)):
        df.loc[i] = [date_query1[i]['created_time'].strftime('%Y-%m'), date_query1[i]['c']]

    grodf1 = df.groupby('one').sum()
    lisdic1 = []
    n = 0
    for gro in grodf1.two:
        lisdic1.append({'one': grodf1.two.index[n], 'two':gro, 'three': datetime.strptime(grodf1.two.index[n], '%Y-%m')})
        n += 1
    lisdic1.reverse()
    return {
        'date_list': lisdic1
    }


# 侧边栏标签云
@register.inclusion_tag('blog/inclusions/_tags.html', takes_context=True)
def show_tags(context):
    return {
        'tag_list': Tag.objects.all().annotate(c=Count('post')), # .filter(c__gt=0) 过滤掉小于1的标签
    }


# 侧边栏点击数
@register.inclusion_tag('blog/inclusions/_views_max.html', takes_context=True)
def show_views_max(context, num=5):
    return {
        'views_max_list': Post.objects.all().order_by('-views')[:num],
    }


