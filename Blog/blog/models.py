from django.urls import reverse
from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class Master(models.Model):
    name = models.CharField("姓名",max_length=20)
    email = models.EmailField("邮箱",max_length=50,blank = True,null=True)
    mobile = models.CharField("电话",max_length=11,blank = True,null=True)
    jobnum = models.CharField("工号",max_length=11,blank = True,null=True)
    job = models.CharField("业务",max_length=100,blank = True,null=True)
    where = models.CharField("是否上班",choices=(('休息','休息'),('上班','上班')),max_length=4,null=True,blank=True)
    others = models.CharField("其他",max_length=100,blank = True,null=True)

    def get_absolute_url(self):
        return reverse('blog:master',args=[str(self.id)])
    class Meta:
        verbose_name = "业务担当"
        verbose_name_plural = verbose_name 
        ordering = ['id']
    def __str__(self):
        return self.job

class User(AbstractUser):
    avatar = models.ImageField(upload_to = 'avatar/%Y/%m',default ='/media/default.jpeg',max_length = 200,blank=True,null = True,verbose_name='头像')
    qq = models.CharField(max_length=20,blank=True,null=True,verbose_name='QQ号码')
    mobile = models.CharField(max_length = 11,blank = True,null = True,unique=True,verbose_name='手机号码')
    jobnum = models.CharField(max_length = 10,blank=True,null=True,verbose_name='工号')

    class Meta:
        verbose_name = '用户'
        verbose_name_plural = verbose_name
        ordering = ['id']
    def __str__(self):
        return self.username

class Tag(models.Model):
    name = models.CharField(max_length = 30,verbose_name = '标签名称')

    class Meta:
        verbose_name = "标签"
        verbose_name_plural = verbose_name 
    
    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length = 30,verbose_name = '分类名称')
    index = models.IntegerField(default = 999,verbose_name = '分类的排序')

    class Meta:
        verbose_name = '分类'
        verbose_name_plural = verbose_name
        ordering = ['index','id']

    def __str__(self):
        return self.name

class ArticleManager(models.Manager):
    def distinct_date(self):
        distinct_date_list =[]
        date_list = self.values('date_publish')
        for date in date_list:
            date = date['date_publish'].strftime('%Y/%m文章存档')
            if date not in distinct_date_list:
                distinct_date_list.append(date)
        return distinct_date_list

class PublishedArticle(models.Manager):
    def get_queryset(self):
        return super(PublishedArticle,self).get_queryset().filter(is_post=True)


class Article(models.Model):
    title = models.CharField(max_length=50,verbose_name='文章标题')
    desc = models.CharField(max_length=50,verbose_name='文章描述')
    content = models.TextField(verbose_name='文章内容')
    click_count = models.IntegerField(default=0,verbose_name='点击次数')
    is_recommend = models.BooleanField(default=False,verbose_name='是否推荐')
    is_post = models.BooleanField(default=False,verbose_name='是否发表')
    date_publish = models.DateTimeField(auto_now_add=True,verbose_name = '发表时间')
    user = models.ForeignKey(User,verbose_name='用户')
    category  = models.ForeignKey(Category,blank=True,null=True,verbose_name='分类')
    tag = models.ManyToManyField(Tag,verbose_name="标签",max_length=100,blank=True)

    objects = ArticleManager()
    post_objects = PublishedArticle()

    class Meta:
        verbose_name = '文章'
        verbose_name_plural = verbose_name
        ordering = ['-date_publish']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:details',args=[str(self.id)])


class Comment(models.Model):
    content= models.TextField(verbose_name='评论内容')
    username = models.CharField(max_length = 30,blank=True,null=True,verbose_name='用户名')
    email = models.EmailField(max_length=50,blank=True,null=True,verbose_name='邮箱地址')
    jobnum = models.CharField(max_length=10,blank=True,null=True,verbose_name='工号')
    date_publish = models.DateTimeField(auto_now_add=True,verbose_name='发布时间')
    user = models.ForeignKey(User,blank=True,null=True,verbose_name='用户')
    Article = models.ForeignKey(Article,related_name='Comment',blank=True,null=True,verbose_name='文章')
    pid = models.ForeignKey('self',blank=True,null=True,verbose_name='父级评论')

    class Meta:
        verbose_name = '评论'
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.id)	

class Links(models.Model):
    title = models.CharField(max_length=50,verbose_name='标题')
    picurl = models.ImageField(upload_to='link/%Y/%m',verbose_name='图片路径',blank=True,null=True,default='/media/link/default.png')
    description = models.CharField(max_length=200,verbose_name='友情链接描述')
    callback_url = models.URLField(verbose_name='url地址')
    date_publish = models.DateTimeField(auto_now_add=True,verbose_name='发布时间')
    index = models.IntegerField(default=999,verbose_name='排列顺序(从小到大)')

    class Meta:
        verbose_name = '友情链接'
        verbose_name_plural = verbose_name
        ordering = ['index','id']
	
    def __str__(self):
        return self.title

class Ad(models.Model):
    title = models.CharField(max_length=50,verbose_name='广告标题')
    description = models.CharField(max_length=200,verbose_name='公告描述')
    picurl = models.ImageField(upload_to='ad/%Y/%m',verbose_name='图片路径')
    callback_url = models.URLField(null=True,blank=True,verbose_name='回调url')
    date_publish = models.DateTimeField(auto_now_add=True,verbose_name='发布时间')
    index = models.IntegerField(default=999,verbose_name='排列顺序(从小到大)')
    active = models.BooleanField("是否发表",default=True)
    class Meta:
        verbose_name = '广告'
        verbose_name_plural = verbose_name
        ordering = ['index','id']

    def __str__(self):
        return self.title



class Event(models.Model):
    eventlist=(('计算机相关问题','计算机相关问题'),('会议相关问题','会议相关问题'),('电话相关问题','电话相关问题'),('视频监控相关问题','视频监控相关问题'),('餐卡相关问题','餐卡相关问题'))
    gradech = (('0','0'),('菜鸟','菜鸟'),('高手','高手'),('大师','大师'),('宗师','宗师'),('神','神'))
    events = models.CharField('故障',max_length=20,choices=eventlist,default='计算机相关问题')
    eventdetail = models.TextField("故障描述",blank=True)
    jindu = models.BooleanField('收否结束',default=False)
    username = models.CharField("姓名",max_length=30,null=True)
    address = models.CharField("位置",max_length=100,null=True)
    mobile = models.CharField("电话",max_length=11,null = True)
    jobnum = models.CharField("工号",max_length=10,null=True)
    email = models.EmailField("邮箱",max_length=30,null=True)
    user = models.ForeignKey(User,blank=True,null=True,verbose_name='用户')
    worker = models.CharField("IT受理人",max_length=30,default="IT")
    created = models.DateTimeField('创建时间',auto_now_add=True)
    updated = models.DateTimeField('更新',auto_now=True)
    grade = models.CharField('评价',max_length=20,choices=gradech,null=True,blank=True)
    gradetext = models.TextField('建议',blank=True)

    def __str__(self):
        return self.events
       
    def get_absolute_url(self):
        return reverse('blog:eventdetail',args=[str(self.id)])

    class Meta:
        ordering=('-created',)
        verbose_name="故障"
        verbose_name_plural = verbose_name


    










