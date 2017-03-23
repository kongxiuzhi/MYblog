#coding:utf-8
from django.core.paginator import Paginator,InvalidPage,EmptyPage,PageNotAnInteger
from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse,HttpResponseRedirect
from django.db.models import Count
from django.urls import reverse
from django.contrib.auth import logout,login,authenticate
from django.contrib.auth.hashers import make_password
from django.db.models import Count
from .models import *
from .forms import *
#from froms import *
import json
# Create your views here.
def homeview(request):
    return HttpResponseRedirect('/blog/')

def global_setting(request):
    username = request.user if request.user.is_authenticated() else '游客'
    ads = Ad.objects.filter(active = True)
    links = Links.objects.all()
    recommend_articles = Article.post_objects.filter(is_recommend=True)[:4]
    master = Master.objects.all()
    return locals()

def masterview(request,master_id):
    master = get_object_or_404(Master,pk=master_id)
    return render(request,'blog/masterdetail.html',locals())


def logoutview(request):
    logout(request)
    ua = request.META.get('HTTP_REFERER','/blog/')
    return HttpResponseRedirect(ua)

def loginview(request):
    if request.method=='POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            user = authenticate(username=username,password=password)
            if user is not None:
                user.backend = 'django.contrib.auth.backends.ModelBackend'
                login(request,user)
            else:
                return render(request,'blog/error.html',{'reason':'登录验证失败'})
            return HttpResponseRedirect('/blog/')
        else:
            return render(request,'blog/error.html',{'reason':login_form.errors})
    else:
       loginform = LoginForm()
    return render(request,'blog/login.html',locals())

def registview(request):
    if request.method =="POST":
        reg_form = RegForm(request.POST)
        if reg_form.is_valid():
            username = reg_form.cleaned_data['username']
            email = reg_form.cleaned_data['email']
            jobnum = reg_form.cleaned_data['jobnum']
            password = make_password(reg_form.cleaned_data['password'])
            user =User.objects.create(username=username,email=email,jobnum=jobnum,password=password)
            user.backend = 'django.contrib.auth.backends.ModelBackend'
            login(request,user)
            return HttpResponseRedirect('/blog/')
        else:
            return render(request,'blog/error.html',{'reason':reg_form.errors})

    else:
        regform = RegForm()
    return render(request,'blog/regist.html',locals())



def getPage(request,article_list):
    pages = Paginator(article_list,4)
    try:
        page = int(request.GET.get('page',1))
        article_list = pages.page(page)
    except(EmptyPage,InvalidPage,PageNotAnInteger):
        article_list = pages.page(1)
    return article_list

def indexview(request):
    article_list = Article.post_objects.annotate(comnum = Count('Comment'))
    article_list = getPage(request,article_list)
    return render(request,'blog/index.html',{'page':article_list})


def detailsview(request,article_id):
    if request.method == 'POST':
        commentform = CommentForm(request.POST)
        if commentform.is_valid():
            username = commentform.cleaned_data['author']
            email = commentform.cleaned_data['email']
            jobmun = commentform.cleaned_data['jobnum']
            content = commentform.cleaned_data['comment']
            user = request.user if request.user.is_authenticated() else None
            Comment.objects.create(username = username,email = email,jobnum = jobnum,content = content,Article_id = article_id,user = user)
        else:
            return HttpResponse('fail')
        return HttpResponseRedirect('/blog/')
        
    try:
        article = Article.post_objects.get(id=article_id)
        article.click_count+=1
        article.save()
    except Article.DoesNotExists:
        return render(request,'blog/error.html',{'reason':'没有找到对应的文章！'})
    comment_form = CommentForm(
                                {'authon':request.user.username,
                                 'email':request.user.email,
                                 'jobnum':request.user.jobnum,
                                }if request.user.is_authenticated() else {})

    comments = Comment.objects.filter(Article=article).order_by('-id')
    comment_plist = []
    comment_slist = []
    for comment in comments:
        if comment.pid is None:
            if not hasattr(comment,'children_comment'):
                setattr(comment,'children_comment',[])
            comment_plist.append(comment)
        else:
            comment_slist.append(comment)
    for comment in comment_slist:
        for item in comment_plist:
            if comment.pid == item:
                item.children_comment.append(comment)
                break
    return render(request,'blog/detail.html',locals())


def eventview(request):

    if request.user.is_authenticated():
        user = User.objects.get(username = request.user)
        myevents = Event.objects.filter(user=str(user.id),jindu=False)
        myevents_done = Event.objects.filter(user=str(user.id),jindu=True)

    else:
        return HttpResponse('请注册!')
    if request.method =='POST':
        event_form = EventForm(request.POST)
        if event_form.is_valid():
            ev = event_form.save(commit = False)
            ev.user = request.user
            ev.save()
            return HttpResponseRedirect('/blog/event/')
        else:
            return render(request,'blog/error.html',{'reason':"提交失败，重新提交"})
    else:
        eventform = EventForm(initial={
                                 "username":user.username,
                                 "email":user.email,
                                 "mobile":user.mobile,
                                 "jobnum":user.jobnum,
                                        })
    return render(request,'blog/event.html',locals())


def eventdetailview(request,event_id):
    if request.method=="POST":
        gradeform = GradeForm(request.POST)
        if gradeform.is_valid():
            grade = gradeform.cleaned_data['grade']
            gradetext = gradeform.cleaned_data['gradetext']
            event = Event.objects.get(pk=event_id)
            event.grade=grade
            event.gradetext = gradetext
            event.save()
            return HttpResponseRedirect('/blog/event/')
        else:
            return render(request,'blog/error.html',{'reason':'请重新提交'})
    else:
        event = Event.objects.get(pk=event_id)
        gradeform = GradeForm()
        return render(request,'blog/eventdetail.html',locals())
        
        

'''
        with open('/home/py3env/Blog/media/log.txt','a',encoding='utf-8') as f:
            for item in myevents:
                f.write(str(item.events))

            '''
