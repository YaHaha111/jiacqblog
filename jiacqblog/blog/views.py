import re, markdown
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models.aggregates import Count, Sum
from django.shortcuts import render, get_object_or_404
from .models import Post, Category, Tag, Blog_panel, Bigcategory
from markdown.extensions.toc import TocExtension
from django.utils.text import slugify

from userinfo.views import save_ip


def demo(request):
    return render(request, 'demo/index.html')


def index(request):
    save_ip(request)

    post_list_all = Post.objects.all().order_by('-created_time')
    paginator = Paginator(post_list_all, 7, 1)  # 每页显示 7 篇， 最后一页少于 1 篇则并入上一页
    page = request.GET.get('page')
    try:
        post_list = paginator.page(page)
    except PageNotAnInteger:
        # 如果用户请求的页码号不是整数，显示第一页
        post_list = paginator.page(1)
    except EmptyPage:
        # 如果用户请求的页码号超过了最大页码号，显示最后一页
        post_list = paginator.page(paginator.num_pages)


    post_count = post_list_all.count()
    img_url = Blog_panel.objects.filter(id=1).values('name', 'index_img', 'motto')
    return render(request, 'blog/index.html', context={'post_list': post_list,
                                                       'post_count': post_count,
                                                       'img_url': img_url
                                                       })


def detail(request, pk):
    save_ip(request)

    post = get_object_or_404(Post, pk=pk)

    # 每调用一次，阅读量 +1
    post.increase_views()

    md = markdown.Markdown(extensions=[
        # 包含 缩写、表格等常用扩展
        'markdown.extensions.extra',
        # 语法高亮扩展
        'markdown.extensions.codehilite',
        'markdown.extensions.toc',
        # 引入标题的值到URL
        TocExtension(slugify=slugify),
    ])
    post.body = md.convert(post.body)

    # 使用正则表达式匹配文章中是否存在目录标题
    m = re.search(r'<div class="toc">\s*<ul>(.*)</ul>\s*</div>', md.toc, re.S)
    post.toc = m.group(1) if m is not None else ''

    return render(request, 'blog/detail.html', context={'post': post})


def archive(request, year, month):
    save_ip(request)

    post_list_all = Post.objects.filter(created_time__year=year,
                                       created_time__month=month
                                       ).order_by('-created_time')

    paginator = Paginator(post_list_all, 7, 1)  # 每页显示 7 篇， 最后一页少于 1 篇则并入上一页
    page = request.GET.get('page')
    try:
        post_list = paginator.page(page)
    except PageNotAnInteger:
        # 如果用户请求的页码号不是整数，显示第一页
        post_list = paginator.page(1)
    except EmptyPage:
        # 如果用户请求的页码号超过了最大页码号，显示最后一页
        post_list = paginator.page(paginator.num_pages)

    yMon_day = str(year) + "年" + str(month) + "月归档"
    return render(request, 'blog/content.html', context={'post_list': post_list,
                                                         'yMon_day': yMon_day,
                                                         })


# 定义筛选出指定标签的文档
def tag(request, pk):
    save_ip(request)

    t = get_object_or_404(Tag, pk=pk)
    post_list_all = Post.objects.filter(tags=t).order_by('-created_time')
    content_sum = Post.objects.filter(tags=t).aggregate(content_int=Sum('content_int'))
    yMon_day = t

    paginator = Paginator(post_list_all, 7, 1)  # 每页显示 7 篇， 最后一页少于 1 篇则并入上一页
    page = request.GET.get('page')
    try:
        post_list = paginator.page(page)
    except PageNotAnInteger:
        # 如果用户请求的页码号不是整数，显示第一页
        post_list = paginator.page(1)
    except EmptyPage:
        # 如果用户请求的页码号超过了最大页码号，显示最后一页
        post_list = paginator.page(paginator.num_pages)

    return render(request, 'blog/content.html', context={'post_list': post_list,
                                                         'yMon_day': yMon_day,
                                                         'content_sum': content_sum['content_int'],
                                                         })


def category(request, pk):
    save_ip(request)

    t = get_object_or_404(Category, pk=pk)
    post_list_all = Post.objects.filter(category=t).order_by('-created_time')
    content_sum = Post.objects.filter(category=t).aggregate(content_int=Sum('content_int'))
    yMon_day = t

    paginator = Paginator(post_list_all, 7, 1)  # 每页显示 7 篇， 最后一页少于 1 篇则并入上一页
    page = request.GET.get('page')
    try:
        post_list = paginator.page(page)
    except PageNotAnInteger:
        # 如果用户请求的页码号不是整数，显示第一页
        post_list = paginator.page(1)
    except EmptyPage:
        # 如果用户请求的页码号超过了最大页码号，显示最后一页
        post_list = paginator.page(paginator.num_pages)

    return render(request, 'blog/content.html', context={'post_list': post_list,
                                                         'yMon_day': yMon_day,
                                                         'content_sum': content_sum['content_int'],

                                                         })


def categories_menu(request):
    save_ip(request)

    return render(request, 'blog/findmenu/categories_menu.html', context={
        'category_list': Category.objects.all().annotate(c=Count('post')).filter(c__gt=0), # 去除小于1的
        'bigcategory_list': Bigcategory.objects.all().annotate(c=Count('category')).filter(c__gt=0),
    })


def tags_menu(request):
    save_ip(request)

    return render(request, 'blog/findmenu/tags_menu.html', context={
        'tag_list': Tag.objects.all().annotate(c=Count('post')), # .filter(c__gt=0) 过滤掉小于1的标签
    })


def archives_menu(request):
    save_ip(request)

    if request.POST:
        if request.POST['min_day'] > request.POST['max_day']:
            min_day = request.POST['min_day']
            max_day = request.POST['min_day']
        else:
            min_day = request.POST['min_day']
            max_day = request.POST['max_day']

        post_list_all = Post.objects.filter(created_time__lt=max_day, created_time__gt=min_day).order_by('-created_time')
    else:
        post_list_all = Post.objects.all().order_by('-created_time')

    paginator = Paginator(post_list_all, 20, 3)  # 每页显示 7 篇， 最后一页少于 1 篇则并入上一页
    page = request.GET.get('page')
    try:
        post_list = paginator.page(page)
    except PageNotAnInteger:
        # 如果用户请求的页码号不是整数，显示第一页
        post_list = paginator.page(1)
    except EmptyPage:
        # 如果用户请求的页码号超过了最大页码号，显示最后一页
        post_list = paginator.page(paginator.num_pages)

    return render(request, 'blog/findmenu/archives_menu.html', context={
        'post_list': post_list
    })


