from django.db import models
from django.utils import timezone


class UserIP(models.Model):
    ip = models.CharField('访问IP', max_length=20, unique=True)
    address = models.CharField('访问地址', max_length=300)
    name = models.CharField('用户名', max_length=50)
    email = models.EmailField('邮箱')
    url = models.URLField('网址', null=True, blank=True)
    first_time = models.DateTimeField('第一次访问时间', default=timezone.now)
    last_time = models.DateTimeField('最近访问时间', null=True, blank=True)
    views =  models.IntegerField('访问次数', default=0)

    verbose_name = '访客信息'
    verbose_name_plural = verbose_name

    def __str__(self):
        return self.ip

    # 访问量
    def increase_views(self):
        self.views += 1
        self.last_time = timezone.now()
        self.save(update_fields=['views', 'last_time'])

    # 用户评论信息
    def increase_nameORemail(self, name=None, email=None):
        self.name = name
        self.email = email
        self.save(update_fields=['name', 'email'])


class IP_post(models.Model):
    ip = models.ForeignKey(UserIP, on_delete=models.CASCADE, verbose_name="关联IP")
    like_post = models.ForeignKey('blog.Post', on_delete=models.CASCADE, verbose_name="点赞文章")
    like_time = models.DateTimeField('点赞时间', default=timezone.now)
    first_time = models.DateTimeField('第一次访问文章时间', default=timezone.now)
    last_time = models.DateTimeField('最近访问文章时间')
    views =  models.IntegerField('访问文章次数', default=0)

    # 访问量
    def increase_views(self):
        self.views += 1
        self.last_time = timezone.now()
        self.save(update_fields=['views', 'last_time'])

    class Meta:
        verbose_name = '文章访问情况'
        verbose_name_plural = verbose_name

class IP_comment(models.Model):
    ip = models.ForeignKey(UserIP, on_delete=models.CASCADE, verbose_name="关联IP")
    like_comment = models.ForeignKey('comments.Comment', on_delete=models.CASCADE, verbose_name="点赞的评论")
    like_time = models.DateTimeField('点赞时间', default=timezone.now)

    class Meta:
        verbose_name = '点赞评论'
        verbose_name_plural = verbose_name


class IP_reply(models.Model):
    ip = models.ForeignKey(UserIP, on_delete=models.CASCADE, verbose_name="关联IP")
    like_reply = models.ForeignKey('comments.Reply', on_delete=models.CASCADE, verbose_name="点赞的回复")
    like_time = models.DateTimeField('点赞时间', default=timezone.now)

    class Meta:
        verbose_name = '点赞回复'
        verbose_name_plural = verbose_name



