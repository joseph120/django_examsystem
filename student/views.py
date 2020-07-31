from django.shortcuts import render
from django.shortcuts import render, redirect
from student import models
from django.http import HttpResponse
from django.contrib.auth import logout, login
from django.contrib import admin
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password, check_password
# Create your views here.
import random
from django.http import JsonResponse
import time
import datetime
from django.core import serializers
from django.forms.models import model_to_dict
import json
from django.contrib.auth.decorators import login_required


# @login_required
# def homepage(request):
#     pass

def stratlogin(request):
    return render(request, 'login.html')


def index(request):
    return render(request, 'index.html')


def toIndex(request):
    return render(request, 'login.html')


def userLogin(request):
    if request.method == 'POST':
        # 获取表单信息
        userId = request.POST.get('user_id')
        password = request.POST.get('password')
        shenfen = request.POST.get("denglu")
        print("id", userId, "password", password, "shenfen", shenfen)
        if userId and password:
            if shenfen:  # 通过学号获取该学生实体
                if shenfen == "stu":
                    try:
                        student = models.Student.objects.get(id=userId)
                        if password == student.password:  # 登录成功
                            # 查询考试信息,同个专业同一专业只保留一个考试信息
                            paper = models.Paper.objects.filter(major=student.major).values("subject", "major",
                                                                                            "examtime").distinct()
                            # 查询成绩信息
                            grade = models.Grade.objects.filter(sid=student.id)
                            # 渲染index模板
                            return render(request, 'index.html',
                                          {'student': student, 'paper': paper, 'grade': grade, "message": "欢迎您登录"})
                        else:
                            message = "密码错误"
                    except:
                        message = "学号不存在"
                elif shenfen == "tec":
                    try:
                        teacher = models.Teacher.objects.get(id=userId)
                        if password == teacher.password:  # 登录成功
                            paper = models.Paper.objects.filter(tid=teacher.id)

                            data1 = models.Grade.objects.filter(subject='软件工程', grade__lt=60).count()
                            data2 = models.Grade.objects.filter(subject='软件工程', grade__gte=60, grade__lt=70).count()
                            data3 = models.Grade.objects.filter(subject='软件工程', grade__gte=70, grade__lt=80).count()
                            data4 = models.Grade.objects.filter(subject='软件工程', grade__gte=80, grade__lt=90).count()
                            data5 = models.Grade.objects.filter(subject='软件工程', grade__gte=90).count()

                            data6 = models.Grade.objects.filter(subject='数据库原理', grade__lt=60).count()
                            data7 = models.Grade.objects.filter(subject='数据库原理', grade__gte=60, grade__lt=70).count()
                            data8 = models.Grade.objects.filter(subject='数据库原理', grade__gte=70, grade__lt=80).count()
                            data9 = models.Grade.objects.filter(subject='数据库原理', grade__gte=80, grade__lt=90).count()
                            data10 = models.Grade.objects.filter(subject='数据库原理', grade__gte=90).count()

                            data_1 = {'data1': data1, 'data2': data2, 'data3': data3, 'data4': data4, 'data5': data5}
                            data_2 = {'data6': data6, 'data7': data7, 'data8': data8, 'data9': data9, 'data10': data10}

                            print("数量：", data2)
                            return render(request, 'teacher.html',
                                          {'teacher': teacher, 'paper': paper, 'data_1': data_1, 'data_2': data_2})
                        else:
                            message = "密码错误"
                    except:
                        message = "教工号不存在"
                else:
                    try:
                        super_user = User.objects.get(username=userId)
                        ps = check_password(password, super_user.password)
                        print(ps)
                        if ps:
                            user = authenticate(username=userId, password=password)
                            login(request, user=user)
                            return redirect("/admin")
                        else:
                            message = "密码错误"

                    except:
                        message = "管理员不存在"
            else:
                message = "请选择身份"
        else:
            message = "账号或密码为空"
    return render(request, 'login.html', {'message': message})


def startExam(request):
    # POST方法
    if request.method == "POST":
        sid = request.POST.get('sid')
        print(sid)
        subject1 = request.POST.get('subject')
        major = request.POST.get('major')
        student = models.Student.objects.get(id=sid)
        paper = models.Paper.objects.filter(subject=subject1, major=major)
        examtime = request.POST.get("examtime")
        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
        if now > examtime:
            status = 1
            message = {"status": status}
            return JsonResponse(message)
        elif now < examtime:
            status = 2
            message = {"status": status}
            return JsonResponse(message)
        else:
            status = 3
            message = {"status": status}
            return JsonResponse(message)
    # GET方法
    if request.method == "GET":
        sid = request.GET.get('sid')
        subject1 = request.GET.get('subject')
        major = request.GET.get('major')
        student = models.Student.objects.get(id=sid)
        paper = models.Paper.objects.filter(subject=subject1, major=major)
        # 随机抽卷
        paper1 = random.choice(paper)
        return render(request, 'exam.html', {'student': student, 'paper': paper1, 'subject': subject1})


def changePwd(request):
    if request.method == "POST":
        oldpwd = request.POST.get("oldPwd")
        newpwd = request.POST.get("newPwd")
        repwd = request.POST.get("rePwd")
        if oldpwd:
            pass
        else:
            err_msg = "请输入原始密码"
            status = 1
            message1 = {"status": status, "message": err_msg}
            return JsonResponse(message1)


def calGrade(request):
    if request.method == 'POST':
        # 得到学号和科目
        sid = request.POST.get('sid')
        subject1 = request.POST.get('subject')

        # 重新生成Student实例，Paper实例，Grade实例，名字和index中for的一致，可重复渲染
        student = models.Student.objects.get(id=sid)
        paper = models.Paper.objects.filter(major=student.major)
        grade = models.Grade.objects.filter(sid=student.id)

        # 计算该门考试的学生成绩
        question = models.Paper.objects.filter(subject=subject1).values("pid").values('pid__id', 'pid__answer',
                                                                                      'pid__score')

        mygrade = 0  # 初始化一个成绩为0
        for p in question:
            qId = str(p['pid__id'])  # int 转 string,通过pid找到题号
            myans = request.POST.get(qId)  # 通过 qid 得到学生关于该题的作答
            # print(myans)
            okans = p['pid__answer']  # 得到正确答案
            # print(okans)
            if myans == okans:  # 判断学生作答与正确答案是否一致
                mygrade += p['pid__score']  # 若一致,得到该题的分数,累加mygrade变量

        # 向Grade表中插入数据
        models.Grade.objects.create(sid_id=sid, subject=subject1, grade=mygrade)
        # print(mygrade)
        # 重新渲染index.html模板
        return render(request, 'index.html', {'student': student, 'paper': paper, 'grade': grade})


def showGrade(request):
    subject1 = request.GET.get('subject')
    grade = models.Grade.objects.filter(subject=subject1)

    data1 = models.Grade.objects.filter(subject=subject1, grade__lt=60).count()
    data2 = models.Grade.objects.filter(subject=subject1, grade__gte=60, grade__lt=70).count()
    data3 = models.Grade.objects.filter(subject=subject1, grade__gte=70, grade__lt=80).count()
    data4 = models.Grade.objects.filter(subject=subject1, grade__gte=80, grade__lt=90).count()
    data5 = models.Grade.objects.filter(subject=subject1, grade__gte=90).count()

    data = {'data1': data1, 'data2': data2, 'data3': data3, 'data4': data4, 'data5': data5}

    return render(request, 'showGrade.html', {'grade': grade, 'data': data, 'subject': subject1})


def sendEmail(request):
    if request.method == "POST":
        print(1)
        email = request.POST.get("email")
        print(email)
        status = 1
        emailmsg = "验证码已发送"
        messag = {'status': status, "message": emailmsg}
        return JsonResponse(messag)


def studentLogin(request):
    pass


def teacherLogin(request):
    pass


def logOut(request):
    return redirect('/toIndex/')
