from django.db import models
from django.utils import timezone


class Comment(models.Model):
    name = models.CharField('用户名', max_length=50)
    email = models.EmailField('邮箱')
    url = models.URLField('网址', null=True, blank=True)
    text = models.TextField('评论内容')
    created_time = models.DateTimeField('创建时间', default=timezone.now)
    post = models.ForeignKey('blog.Post', verbose_name='文章', on_delete=models.CASCADE)
    good_count = models.IntegerField(default=0, db_column='gcount', verbose_name='好评数')

    class Meta:
        verbose_name = '评论'
        verbose_name_plural = verbose_name

    def __str__(self):
        return '{}: {}'.format(self.name, self.text[:20])


class Reply(models.Model):
    name = models.CharField('用户名',max_length=20)
    email = models.EmailField('邮箱')
    url = models.URLField('网址', null=True, blank=True)
    text = models.TextField('回复内容')
    created_time = models.DateTimeField('创建时间', default=timezone.now)
    rep_com = models.ForeignKey(Comment, on_delete=models.CASCADE, verbose_name="回复")
    reply_again = models.ForeignKey("Reply", default=0, on_delete=models.CASCADE, verbose_name="子回复")
    good_count = models.IntegerField(default=0, db_column='gcount', verbose_name='好评数')

    class Meta:
        verbose_name = '回复'
        verbose_name_plural = verbose_name

