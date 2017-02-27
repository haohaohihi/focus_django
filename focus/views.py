import logging
from django.shortcuts import render
from django.http import HttpResponse
from django.core.paginator import Paginator
from .models import ArticleModel
# Create your views here.

logger = logging.getLogger("focus")


def index(request):
    articles = ArticleModel.objects.filter(article_category="products").order_by('-article_date')
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


def get_page(request, page=1, category="products", sub_category=""):
    articles = ArticleModel.objects.filter(article_category=category,
                                           article_sub_category=sub_category).order_by('-article_date')
    paginator = Paginator(articles, 10)
    page = int(page)
    if page == 1:
        pre_page = page
        next_page = page + 1
    elif page == paginator.num_pages:
        pre_page = page - 1
        next_page = paginator.num_pages
    else:
        pre_page = page - 1
        next_page = page + 1
    page_dict = {
        'articles': paginator.page(1),
        'pre_page': pre_page,
        'next_page': next_page,
        'page': page,
        'pages': paginator.num_pages,
        'category': category,
        'sub_category': sub_category,
    }
    return render(request, 'focus/page.html'.format(category), page_dict)
