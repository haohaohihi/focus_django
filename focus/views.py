import logging
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login
from django.core.paginator import Paginator
from .models import ArticleModel
# Create your views here.

logger = logging.getLogger("focus")


def index(request):
    articles = ArticleModel.objects.filter(article_category="news").order_by('-article_date')
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


def get_page(request, page=1, category="news", sub_category=""):
    logger.info("category: %s; page: %s; sub_category: %s" % (category, page, sub_category))
    if sub_category != "":
        articles = ArticleModel.objects.filter(article_category=category,
                                           article_sub_category=sub_category).order_by('-article_date')
    else:
        articles = ArticleModel.objects.filter(article_category=category).order_by('-article_date')
    logger.info("articles num: %s" % len(articles))
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
        'articles': paginator.page(page),
        'pre_page': pre_page,
        'next_page': next_page,
        'page': page,
        'pages': paginator.num_pages,
        'category': category,
        'sub_category': sub_category,
    }
    return render(request, 'focus/index.html'.format(category), page_dict)


def login_page(request):
    return render(request, 'focus/login_page.html')


@csrf_exempt
def do_login(request):
    username = str(request.POST.get("username"))
    password = str(request.POST.get("password"))
    logger.info("username: %s" % username)
    logger.info("password: %s" % password)
    user = authenticate(username=username, password=password)
    if user is not None:
        login(request, user)
        return HttpResponseRedirect('/')


@csrf_exempt
def register(request):
    username = request.POST.get("username")
    email = request.POST.get("email")
    password = request.POST.get("password")
    confirm_password = request.POST.get("confirm-password")
    user = User.objects.create_user(username=username, email=email, password=password)
    return HttpResponseRedirect('/')

