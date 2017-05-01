from django.contrib import admin
from django.db import models
from .models import UserCollection, Article, User

# Register your models here.


class ArticleAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'article_source', 'article_category', 'article_sub_category', 'get_date')
    list_filter = ('article_source', 'article_category', 'article_sub_category')
    search_fields = ('article_title',)
    ordering = ('-article_date', 'article_title')

    def get_search_results(self, request, queryset, search_term):
        queryset, use_distinct = super(ArticleAdmin, self).get_search_results(request, queryset, search_term)
        try:
            search_term_as_int = int(search_term)
            queryset |= self.model.objects.filter(age=search_term_as_int)
        except:
            pass
        return queryset, use_distinct


class UserAdmin(admin.ModelAdmin):
    list_filter = ('is_staff',)
    list_display = ('username', 'date_joined', 'last_login', 'email')

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Article, ArticleAdmin)