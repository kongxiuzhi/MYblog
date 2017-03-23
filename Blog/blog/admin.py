#coding:utf-8
from django.contrib import admin
from .models import *


# Register your models here.

def make_recommend(self,request,queryset):
    queryset.update(is_recommend=True)

make_recommend.short_description = "推荐文章"



def dis_recommend(modeladmin,request,queryset):
    queryset.update(is_recommend=False)
dis_recommend.short_description = "取消推荐"

def make_published(modeladmin,request,queryset):
    queryset.update(is_post = True)
make_published.short_description = "发表文章"
def dis_published(modeladmin,request,queryset):
    queryset.update(is_post = False)
dis_published.short_description = "取消发表"

class ArticleAdmin(admin.ModelAdmin):
    list_display=('title','desc','is_recommend','is_post','click_count')
    list_display_links = ('title','desc')
    list_editable = ('click_count',)
    actions= [make_recommend,make_published,dis_recommend,dis_published]


    fieldsets = (
			(None,{
				'fields':('title','desc','content','user','category','tag')
				}),
			('高级设置',{
				'classes':('collapse',),
				'fields':('click_count','is_recommend','is_post',),
				}),
		)
    class Media:
        js =(
            'js/kindeditor/kindeditor-all.js',
            'js/kindeditor/lang/zh_CN.js',
            'js/kindeditor/config.js',)  



admin.site.register(Article,ArticleAdmin)
admin.site.register(User)
admin.site.register(Tag)
admin.site.register(Master)
admin.site.register(Category)
admin.site.register(Comment)
admin.site.register(Links)
admin.site.register(Ad)
admin.site.register(Event)
