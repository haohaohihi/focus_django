from django.db import models

# Create your models here.


class ArticleModel(models.Model):
	article_title = models.CharField(max_length=200)
	article_desc = models.CharField(max_length=1000, null=True, default='')
	article_link = models.URLField()
	article_source = models.CharField(max_length=50)
	article_date = models.IntegerField()
	article_category = models.CharField(max_length=50)
	article_sub_category = models.CharField(max_length=50, null=True, default='')
	picture_link = models.URLField(null=True, default='')

	class Meta:
		db_table = 'article'
