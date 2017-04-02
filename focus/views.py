import json
import time
import logging
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from .models import Article, UserCollection
# Create your views here.

logger = logging.getLogger("focus")


def index(request):
    articles = Article.objects.filter(article_category="news").order_by('-article_date')
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
        articles = Article.objects.filter(article_category=category,
                                           article_sub_category=sub_category).order_by('-article_date')
    else:
        articles = Article.objects.filter(article_category=category).order_by('-article_date')
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
    if password != confirm_password:
        result = {
            'status': 1,
            'message': '密码不一致'
        }
        return HttpResponse(json.dumps(result))
    if '@' not in email:
        result = {
            'status': 2,
            'message': '邮箱格式错误'
        }
        return HttpResponse(json.dumps(result))
    user = User.objects.create_user(username=username, email=email, password=password)
    result = {
        'status': 0,
        'message': '注册成功，请登陆'
    }
    return HttpResponse(json.dumps(result))

@csrf_exempt
def do_logout(request):
    logout(request)
    return HttpResponseRedirect('/')


@login_required(login_url='/login_page/')
@csrf_exempt
def change_article_collection(request):
    try:
        user_id = request.user.id
        article_id = request.POST.get("article_id")
        valid = request.POST.get("valid", False)
    except Exception as e:
        logger.error(e)
        result = {
            'status': -1,
            'message': "参数错误"
        }
        return HttpResponse(json.dumps(result))

    try:
        user = User.objects.get(id=user_id)
        article = Article.objects.get(id=article_id)
    except Exception as e:
        logger.error(e)
        result = {
            'status': -2,
            'message': "未查询到用户或文章信息"
        }
        return HttpResponse(json.dumps(result))

    time_now = int(time.time())
    try:
        collection = UserCollection.objects.get(user=user, article=article)
        collection.valid = valid
        collection.last_change_time = time_now
        collection.save()
    except Exception as e:
        collection = UserCollection.objects.create(user=user, article=article, valid=valid,
                                                   add_time=time_now, last_change_time=time_now)
        logger.info("create a new collection, id is: %s" % collection.id)
    result = {
        'status': 0,
        'message': "收藏或取消收藏成功"
    }
    return HttpResponse(json.dumps(result))