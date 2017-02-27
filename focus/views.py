import logging
from django.shortcuts import render
from django.http import HttpResponse
from django.core.paginator import Paginator
from .models import ArticleModel
# Create your views here.

logger = logging.getLogger("focus")


def index(request):
	logger.info("test logging")
	articles = ArticleModel.objects.filter(article_category="products")
	paginator = Paginator(articles, 10)
	page = 1
	page_dict = {
		'articles': paginator.page(1),
		'pre_page': page,
		'next_page': page + 1,
		'page': page,
		'pages': paginator.num_pages,
	}
	return render(request, 'focus/index.html', page_dict)


def products_page(request, page):
	return index(request)


def news_page(request, page):
	return index(request)


def design_page(request, page):
	return index(request)


def marketing_page(request, page):
	return index(request)


def dev(request):
	return index(request)


def dev_web_page(request, page):
	return index(request)


def dev_python_page(request, page):
	return index(request)


def dev_linux_page(request, page):
	return index(request)


def dev_db_page(request, page):
	return index(request)


def dev_android_page(request, page):
	return index(request)

