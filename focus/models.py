from django.db import models

# Create your models here.


class ArticleModel(models.Model):
	article_title = models.CharField(max_length=200)
	article_desc = models.CharField(max_length=1000, blank=True)
	article_link = models.URLField(null=True)
	article_source = models.CharField(max_length=50)
	article_date = models.IntegerField()
	article_category = models.CharField(max_length=50, blank=True)
	picture_link = models.URLField(null=True, blank=True)

	class Meta:
		db_table = 'article'
