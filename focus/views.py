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
    user_id = request.user.id
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
    if user_id:
        collections = UserCollection.objects.filter(user_id=user_id, valid=1)
        collections_article_id = [c.article.id for c in collections]
        page_dict['collections_article_id'] = collections_article_id
        logger.info("collections: %s" % collections_article_id)
    return render(request, 'focus/index.html', page_dict)


def get_page(request, page=1, category="news", sub_category=""):
    user_id = request.user.id
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
    if user_id:
        collections = UserCollection.objects.filter(user_id=user_id, valid=1)
        collections_article_id = [c.article.id for c in collections]
        page_dict['collections_article_id'] = collections_article_id

    return render(request, 'focus/index.html', page_dict)


def login_page(request):
    return render(request, 'focus/login_page.html')


@csrf_exempt
def do_login(request):
    username = str(request.POST.get("username"))
    password = str(request.POST.get("password"))
    logger.debug("username: %s" % username)
    logger.debug("password: %s" % password)
    user = authenticate(username=username, password=password)
    if user is not None:
        login(request, user)
        logger.info("login success")
        result = {
            'status': 0,
            'message': '登陆成功！'
        }
    else:
        logger.info("login fail")
        result = {
            'status': 3,
            'message': '密码错误！'
        }
    return HttpResponse(json.dumps(result))


@csrf_exempt
def do_register(request):
    username = request.POST.get("username")
    email = request.POST.get("email")
    password = request.POST.get("password")
    confirm_password = request.POST.get("confirm_password")
    if User.objects.filter(username=username):
        result = {
            'status': 1,
            'message': '用户名已被注册'
        }
        return HttpResponse(json.dumps(result))
    if User.objects.filter(email=email):
        result = {
            'status': 1,
            'message': '邮箱已被注册'
        }
        return HttpResponse(json.dumps(result))
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
def add_or_cancel_collection(request):
    try:
        user_id = request.user.id
        article_id = request.POST.get("article_id")
        valid = int(request.POST.get("valid", 0))
        logger.info("user_id:{0}\narticle_id:{1}\nvalid:{2}".format(
            user_id, article_id, valid))
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


@login_required(login_url='/login_page/')
def my_collections(request, page=1):
    user_id = request.user.id
    if not user_id:
        return HttpResponseRedirect('/login_page')
    try:
        user = User.objects.get(id=user_id)
    except Exception as e:
        logger.error(e)
        return HttpResponseRedirect('/login_page')
    collections = UserCollection.objects.filter(user=user, valid=1)
    collections_article_id = [c.article.id for c in collections]
    articles = Article.objects.filter(id__in=collections_article_id)

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
        'category': "collections",
        'sub_category': "collections",
        'collections_article_id': collections_article_id
    }
    return render(request, 'focus/index.html', page_dict)


def do_search(request):
    user_id = request.user.id
    q_string = str(request.GET.get(('q'), ''))
    articles = Article.objects.filter(article_title__contains=q_string).order_by('-article_date')
    logger.info("Search %s , has %d results" % (q_string, len(articles)))
    paginator = Paginator(articles, 10)
    page = 1
    next_page = page + 1
    pre_page = page - 1
    page_dict = {
        'articles': paginator.page(page),
        'pre_page': pre_page,
        'next_page': next_page,
        'page': page,
        'pages': paginator.num_pages,
        'category': "search",
        'search_string': q_string
    }
    if user_id:
        collections = UserCollection.objects.filter(user_id=user_id, valid=1)
        collections_article_id = [c.article.id for c in collections]
        page_dict['collections_article_id'] = collections_article_id
    return render(request, 'focus/index.html', page_dict)


def search(request, page=1, q_string=""):
    user_id = request.user.id
    logger.info(page, q_string)
    articles = Article.objects.filter(article_title__contains=q_string).order_by('-article_date')
    logger.info("Search %s , has %d results" % (q_string, len(articles)))

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
        'category': "search",
        'search_string': q_string
    }
    if user_id:
        collections = UserCollection.objects.filter(user_id=user_id, valid=1)
        collections_article_id = [c.article.id for c in collections]
        page_dict['collections_article_id'] = collections_article_id

    return render(request, 'focus/index.html', page_dict)