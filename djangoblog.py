'''
django BLOG 总结

'''

1.setting配置

	DEBUG = True|False

	ALLOWED_HOST = ['*']

	app注册：
	     INSTALL_APPS =[
	     	'myapp.apps.MappConfig',

	     ]

	templates位置：
		1：各个APP的根目录 myapp/templates
		2：project 的根目录 Myproject/templates
			配置settings:
				TEMPLATES = [
					{
						'DIRS':[os.path.join(BASW_DIR,'templates')]
					}
				]
		3.全局template:
			TEMPLATES = [
						{
							'DIRS':[os.path.join(BASW_DIR,'templates')]
							'OPTIONS':{

									'myapp.views.global_setting'
							}
						}
					]
			在myapp/views.py下创建：
				from django.conf import settings
				def global_setting(request):
					return locals()
	数据库配置：
		工具：Navicat
		postgresql:
			sudo apt-get install postgresql
			pip install psycopg2
			更改postgres用户密码：
				sudo -u postgres psql
				ALTER USER postgres WITH PASSWORD '123456';
			postgres登陆：
				psql -h 127.0.0.1 -U postgres
			修改ubuntu root登陆postgres密码：
				su root
				sudo passwd -d postgres//删除密码
				sudo -u postgres passwd //设置密码
			重启服务：
				/etc/init.d/postgresql restart//默认端口：5432
			创建用户：
				create user "username" with password "passwords";
				create database "testdb" with owner = "username";
			settings配置：
				DATABASES = {
					'default':{
						'ENGINE':'django.db.backends.postgresql',
						'NAME':'database_name',
						'USER':'database_user_name',
						'PASSWORD':'database_user_password',
						'HOST':'database_service_ip',
						'PORT':'database_port',//'5432'
					}
				}
		msql:
			sudo apt-get install mysql-server
			sudo apt-get install mysql-client
			sudo apt-get install mysql-div
			驱动程序：
				MySQLdb,mysqlclient,mysqlclient(mysql官方推荐)，PyMySQL(纯python)
				pip install PyMySQL
				关键是这里：我们还需要在myproject的__init__.py文件中添加如下的内容：
				import pymusql
				pymysql.install_as_MySQLdb()

	时区设置：
		pip install pytz
		settings配置：
			TIME_ZONE = 'Asia/Shanghai'
			USE_TZ = False

	静态文件配置：
		STATIC_RUL = '/static/'
		STATICFILES_DITS = (os.path.join(BASE_DIR,'static'),)// python manage.py collectstatic
		STATIC_ROOT = '/static/'

	配置上传文件件：
		MEDIA_URL = '/media/'
		MEDIA_ROOT = os.path.join(BASE_DIR,'media')
		权限设置：
			例如：/media/uploads为上传文件夹
			则：cd /media
			sudo chgrp -R www-data uploads
			sudo chmod -R g+w uploads
			一般目录权限设置为 755，文件权限设置为 644 
			假如项目位置在 /home/tu/zqxt （在zqxt 下面有一个 manage.py，zqxt 是项目名称）
			cd /home/tu/
			sudo chmod -R 644 zqxt
			sudo find zqxt -type d -exec chmod 755 \{\} \;
2.User扩展：
	在settings.py下添加：AUTH_USER_MODEL = 'Myapp.User'
	在Myapp.models下：
		from django.contrib.auth.models import AbstractUser
		class User(AbstractUser):
			mobile = models.CharField(max_length=11, blank=True, null=True, unique=True, verbose_name='手机号码')
			class Meta:
        		verbose_name = '用户'
        		verbose_name_plural = verbose_name
        	def __unicode__(self):
        		return self.username
    在Myapp.admin下：
		from django.contrib import admin
		from web_sso import models
		from django.contrib.auth.admin import UserAdmin  # 从django继承过来后进行定制
		from django.utils.translation import ugettext_lazy as _
		from django.contrib.auth.forms import UserCreationForm, UserChangeForm # admin中涉及到的两个表单




		# custom user admin
		class MyUserCreationForm(UserCreationForm):  # 增加用户表单重新定义，继承自UserCreationForm
		    def __init__(self, *args, **kwargs):
		        super(MyUserCreationForm, self).__init__(*args, **kwargs)
		        self.fields['email'].required = True   # 为了让此字段在admin中为必选项，自定义一个form
		        self.fields['mobile'].required = True  # 其实这个name字段可以不用设定required，因为在models中的MyUser类中已经设定了blank=False，但email字段在系统自带User的models中已经设定为
		        # email = models.EmailField(_('email address'), blank=True)，除非直接改源码的django（不建议这么做），不然还是自定义一个表单做一下继承吧。


		class MyUserChangeForm(UserChangeForm):  # 编辑用户表单重新定义，继承自UserChangeForm
		    def __init__(self, *args, **kwargs):
		        super(MyUserChangeForm, self).__init__(*args, **kwargs)
		        self.fields['email'].required = True
		        self.fields['mobile'].required = True


		class CustomUserAdmin(UserAdmin):
		    def __init__(self, *args, **kwargs):
		        super(CustomUserAdmin, self).__init__(*args, **kwargs)
		        self.list_display = ('username', 'mobile', 'email', 'is_active', 'is_staff', 'is_superuser')
		        self.search_fields = ('username', 'email', 'mobile')
		        self.form = MyUserChangeForm  #  编辑用户表单，使用自定义的表单
		        self.add_form = MyUserCreationForm  # 添加用户表单，使用自定义的表单
		        # 以上的属性都可以在django源码的UserAdmin类中找到，我们做以覆盖

		    def changelist_view(self, request, extra_context=None):  # 这个方法在源码的admin/options.py文件的ModelAdmin这个类中定义，我们要重新定义它，以达到不同权限的用户，返回的表单内容不同
		        if not request.user.is_superuser:  # 非super用户不能设定编辑是否为super用户
		            self.fieldsets = ((None, {'fields': ('username', 'password',)}),
		                              (_('Personal info'), {'fields': ('mobile', 'email')}),  # _ 将('')里的内容国际化,这样可以让admin里的文字自动随着LANGUAGE_CODE切换中英文
		                              (_('Permissions'), {'fields': ('is_active', 'is_staff', 'groups')}),
		                              (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
		                              )  # 这里('Permissions')中没有'is_superuser',此字段定义UserChangeForm表单中的具体显示内容，并可以分类显示
		            self.add_fieldsets = ((None, {'classes': ('wide',),
		                                          'fields': ('username', 'mobile', 'password1', 'password2', 'email', 'is_active',
		                                                     'is_staff', 'groups'),
		                                          }),
		                                  )  #此字段定义UserCreationForm表单中的具体显示内容
		        else:  # super账户可以做任何事
		            self.fieldsets = ((None, {'fields': ('username', 'password',)}),
		                              (_('Personal info'), {'fields': ('mobile', 'email')}),
		                              (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups')}),
		                              (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
		                              )
		            self.add_fieldsets = ((None, {'classes': ('wide',),
		                                          'fields': ('username', 'mobile', 'password1', 'password2', 'email', 'is_active',
		                                                     'is_staff', 'is_superuser', 'groups'),
		                                          }),
		                                  )
		        return super(CustomUserAdmin, self).changelist_view(request, extra_context)


		admin.site.register(models.MyUser, CustomUserAdmin)  # 注册一下
3.models
	1.创建绝对路由


		from django.urls import reverse
			def get_absolute_url(self):
				return reverse('app_name:urlname',args=[str(self.id)])
	2.创建admin中的别名：
		class Meta:
			verbose_name = "name"
			verbose_name_plural = verbose_name
	3.字段Choices：
		((),(),()),default=
	4.null,blank
		null数据库可以为空，blank表单可以为空
	5.ImageField
		1.在你的settings文件中, 你必须要定义 MEDIA_ROOT 作为Django存储上传文件的路径(从性能上考虑，这些文件不能存在数据库中。) 
		  定义一个 MEDIA_URL 作为基础的URL或者目录。确保这个目录可以被web server使用的账户写入。
		2.在模型中添加FileField 或 ImageField 字段, 定义 upload_to参数，内容是 MEDIA_ROOT 的子目录，用来存放上传的文件。
		3.数据库中存放的仅是这个文件的路径 （相对于MEDIA_ROOT). 你很可能会想用由Django提供的便利的url 属性。
		  比如说, 如果你的ImageField 命名为 mug_shot, 你可以在template中用 {{ object.mug_shot.url }}获得你照片的绝对路径。
		例如，如果你的 MEDIA_ROOT设定为 '/home/media'，并且 upload_to设定为 'photos/%Y/%m/%d'。
		 upload_to的'%Y/%m/%d'被strftime()所格式化；'%Y' 将会被格式化为一个四位数的年份, '%m' 被格式化为一个两位数的月份'%d'是两位数日份。
		 如果你在Jan.15.2007上传了一个文件，它将被保存在/home/media/photos/2007/01/15目录下.
	6.创建数据记录：
		1. Article.objects.create(title="title")
		2. at=Article(title="title")
			at.save()
		3.at = Article.objects.get(title="tilte")
		  at= Article.objects.get(pk=1)
		  at= Article.objects.filter(title="tilte")
		  at = Article.objects.value("title")
		  form django.db.models import Count
		  at.Count
		  at = Article.objects.annotate(num_book=Count('book'))
		  at.num_book
4.admin
	自定义ACTIONS:
		def make_active(self,request,queryset):
			queryset.update(modelsfie = "推荐")
		make_recommend.short_description = "推荐文章"
		class MyMoelsAdmin(admin.ModelAdmin):
			actions =[make_active,]
	list_display =()
	search_fields = ()
	fields =()
	fieldsets ={
				("title",{'fields':('','')}),
				(None,{"fields":('','')}),
				(None,{'class':('wide',),"fields":('','')}),
		}
				

  	admin.site.register(mymodel,MyMoelsAdmin)
5.form
	class MyForm(forms.Form):
		email = forms.EmailField(widget=forms.TextInput(max_length=50,error_messages={'required':"message"},
								attrs={
											'id':"email",'class':"email",
											'type':'email','size':'25',
											'required':'required','tabindex':'1',
										}))

	class MyForm(forms.ModelForm):
		class Meta:
			model = mymodel
			fields = ('name','password','content')
			widgets = {
				'name':forms.TextInput(max_length=50,error_messages={'required':'message'},
								attrs={'':}
								)
				'content':forms.Textarea(attrs={'cols':'50','rows':'5','placeholder':'请输入内容'})
			}		

	<form action="" method="post">
		{{csref_token}}
		{{myform.as_p}}
		<input type="submit" value="Submit"/>
	</form>	
6.templates
	{%load staticfiles %}
	{% extends 'base.html'%}
	{%include 'ot.html'%}
	{% block content%}{%endblock%}
	{%for in %}{%endfor%}
	{%with as%}{%endwith%}
	{%if is not %}{%elif %}{%else%}{%endif%}
	{{content|safe|linebreaks|truncatechars|date:'Y-m-d'}}
7.login logout
	from django.contrib.auth import logout,login,authenticate
	from django.contrib.auth.hashers import make_password

	def logoutview(request):
		logout(request)
		return render()
	def loginview(request):
		user = authenticate(username,password)
		if user:
			user.backend = 'django.contrib.auth.backends.ModelBackend'
			login(request,user)
	if request.user.is_authenticated()://判断是否登陆
	获得登陆的用户名：name = request.user.username
8.富文本编辑器kindedtor
	1.在admin.py要使用富文本编辑器的（modeladmin）中添加：
		class Media:
		  	js = (
		  			'kindeditor-all.js',
		  			'lang/zh_CN.js',
		  			'myconfig.js'
			  		)
	2.myconfig.js
			kindeditor.ready(function(K){
				K.create('textarea[name=content]',
					{width:'800px',
					 height:'200px',
					 uploadJson:'/admin/media/kindeditor',
					});
				})
	3.url.py
		    url(r"^uploads/(?P<path>.*)$","django.views.static.serve",{"document_root": settings.MEDIA_ROOT,}),
    		url(r'^admin/upload/(?P<dir_name>[^/]+)$', upload_image, name='upload_image'),
    4.upload.py
    		# -*- coding: utf-8 -*-
			from django.http import HttpResponse
			from django.conf import settings
			from django.views.decorators.csrf import csrf_exempt
			import os
			import uuid
			import json
			import datetime as dt

			@csrf_exempt
			def upload_image(request, dir_name):
			    ##################
			    #  kindeditor图片上传返回数据格式说明：
			    # {"error": 1, "message": "出错信息"}
			    # {"error": 0, "url": "图片地址"}
			    ##################
			    result = {"error": 1, "message": "上传出错"}
			    files = request.FILES.get("imgFile", None)
			    if files:
			        result =image_upload(files, dir_name)
			    return HttpResponse(json.dumps(result), content_type="application/json")

			#目录创建
			def upload_generation_dir(dir_name):
			    today = dt.datetime.today()
			    dir_name = dir_name + '/%d/%d/' %(today.year,today.month)
			    if not os.path.exists(settings.MEDIA_ROOT + dir_name):
			        os.makedirs(settings.MEDIA_ROOT + dir_name)
			    return dir_name

			# 图片上传
			def image_upload(files, dir_name):
			    #允许上传文件类型
			    allow_suffix =['jpg', 'png', 'jpeg', 'gif', 'bmp']
			    file_suffix = files.name.split(".")[-1]
			    if file_suffix not in allow_suffix:
			        return {"error": 1, "message": "图片格式不正确"}
			    relative_path_file = upload_generation_dir(dir_name)
			    path=os.path.join(settings.MEDIA_ROOT, relative_path_file)
			    if not os.path.exists(path): #如果目录不存在创建目录
			        os.makedirs(path)
			    file_name=str(uuid.uuid1())+"."+file_suffix
			    path_file=os.path.join(path, file_name)
			    file_url = settings.MEDIA_URL + relative_path_file + file_name
			    open(path_file, 'wb').write(files.file.read()) # 保存图片
			    return {"error": 0, "url": file_url}




