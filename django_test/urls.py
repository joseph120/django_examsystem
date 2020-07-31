"""django_test URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.contrib import admin
from django.urls import path
from django.conf.urls import url
from student import views

urlpatterns = [
    #管理员
    path('admin/', admin.site.urls),
    #url(r'^admin/', admin.site.urls),
    #默认访问首页
    url(r'^$',views.stratlogin),
    #用户登录
    url(r'^userLogin/',views.userLogin),
   # url(r'^$',views.index),
   #  #学生登录
   #  url(r'^studentLogin/',views.studentLogin),
   #  #教师登录
   #  url(r'^teacherLogin/',views.teacherLogin),
    url(r'^showGrade', views.showGrade),
    #url('queryStudent', views.queryStudent),
    url(r'^changePwd',views.changePwd,name="changePwd"),
    url(r'^sendEmail/$', views.sendEmail,name="sendEmail"),
    url(r'^calGrade/$', views.calGrade),
    url(r'^logout/$',views.logOut),
    url(r'^toIndex/$',views.toIndex),
    url(r'^startExam/$',views.startExam,name="startExam"),
]
