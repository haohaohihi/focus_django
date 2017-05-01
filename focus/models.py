import datetime
from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Article(models.Model):
    article_title = models.CharField(max_length=200)
    article_desc = models.CharField(max_length=1000, null=True, default='')
    article_link = models.URLField()
    article_source = models.CharField(max_length=50)
    article_date = models.IntegerField()
    article_category = models.CharField(max_length=50)
    article_sub_category = models.CharField(max_length=50, null=True, default='')
    picture_link = models.URLField(null=True, default='')

    def __str__(self):
        return self.article_title[0:20] + "..."

    def get_date(self):
        return datetime.datetime.fromtimestamp(self.article_date).strftime('%Y-%m-%d')

    class Meta:
        db_table = 'article'


class UserCollection(models.Model):
    user = models.ForeignKey(User)
    article = models.ForeignKey(Article)
    valid = models.BooleanField(default="False")
    add_time = models.IntegerField()
    last_change_time = models.IntegerField()

    def __str__(self):
        return self.user.username

    class Meta:
        db_table = 'user_collection'
        unique_together = (('user', 'article'),)
