import markdown
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from django.utils.html import strip_tags


class Blog_panel(models.Model):
    name = models.CharField('博客名称', max_length=100)
    motto = models.CharField('铭言', max_length=100)
    icon = models.URLField('浏览器小图', blank=False)
    apple_touch_icon = models.URLField('苹果图', blank=False)
    blog_photo = models.URLField('个人头像', blank=False)
    index_img = models.URLField('首页大图', blank=False)
    icp_img = models.URLField('徽标', blank=False)
    zfb_1 = models.URLField('支付宝选项', blank=False)
    zfb_2 = models.URLField('支付宝二维码', blank=False)
    wx_1 = models.URLField('微信选项', blank=False)
    wx_2 = models.URLField('微信二维码', blank=False)
    dmk_img = models.URLField('代码块头部图', blank=True)
    h12_img = models.URLField('代码块h1-h2', blank=True)
    h34_img = models.URLField('代码块h3-h4', blank=True)
    h56_img = models.URLField('代码块h5-h6', blank=True)

    class Meta:
        verbose_name = '博客自定义'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

class Copyright(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = '版权'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Bigcategory(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = '大类'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=100)
    bigcategory = models.ForeignKey(Bigcategory, null=True, on_delete=models.SET_NULL, verbose_name="大类")

    class Meta:
        verbose_name = '分类'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = '标签'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

class Post(models.Model):
    title = models.CharField(max_length=70, verbose_name="标题")
    body = models.TextField(verbose_name="内容")
    created_time = models.DateTimeField(verbose_name="创建时间", default=timezone.now)
    modified_time = models.DateTimeField(verbose_name="修改时间")
    excerpt = models.CharField(max_length=200, blank=True, verbose_name="摘要")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="分类")
    copyright = models.ForeignKey(Copyright, null=True, on_delete=models.SET_NULL, verbose_name="版权")
    usr_name = models.CharField(max_length=70, verbose_name="作者", default=Blog_panel.objects.filter(id=1).values('name')[0]['name'])
    copy_url = models.URLField('原文链接', blank=False, default="www.jcqmxm.com/blog/posts/")
    tags = models.ManyToManyField(Tag, blank=True, verbose_name="标签")
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="作者")
    content_int = models.IntegerField(default=1)
    views = models.PositiveIntegerField(default=0, editable=False)
    img_url = models.URLField('图床网址', blank=False)


    verbose_name = '文章'
    verbose_name_plural = verbose_name

    # 阅读量
    def increase_views(self):
        self.views += 1
        self.save(update_fields=['views'])

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:detail', kwargs={'pk': self.pk})

    def save(self, *args, **kwargs):
        self.modified_time = timezone.now()

        # 首先实例化一个 Markdown 类，用于渲染 body 的文本。
        # 由于摘要并不需要生成文章目录，所以去掉了目录拓展。
        md = markdown.Markdown(extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
        ])

        # 先将 Markdown 文本渲染成 HTML 文本
        # strip_tags 去掉 HTML 文本的全部 HTML 标签
        # 从文本摘取前 54 个字符赋给 excerpt
        self.excerpt = strip_tags(md.convert(self.body))[:70]
        super().save(*args, **kwargs)



class Onemenu(models.Model):
    icon = models.CharField("图标", max_length=100)
    name = models.CharField("菜单名", max_length=100)
    url = models.URLField('网址', blank=True)
    show = models.BooleanField("是否显示子菜单")
    z_width = models.IntegerField("子菜单宽度", default=100)
    order_id = models.IntegerField("排序", default=1)

    class Meta:
        verbose_name = '一级菜单'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name



class Twomenu(models.Model):
    icon = models.CharField("图标", max_length=100)
    name = models.CharField("菜单名", max_length=100)
    url = models.URLField('网址', blank=True)
    onemenu = models.ForeignKey(Onemenu, on_delete=models.CASCADE, verbose_name="关联")
    order_id = models.IntegerField("排序", default=1)

    class Meta:
        verbose_name = '二级菜单'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

