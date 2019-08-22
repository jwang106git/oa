import random

from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse

from .models import Subject, Teacher, User
from .forms import RegisterForm, LoginForm
from util.captcha import Captcha

ALL_CHARS = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'


def show_subjects(request):
    """查看所有学科"""
    subjects = Subject.objects.all()
    return render(request, 'subject.html', {'subjects': subjects})


def show_teachers(request):
    """显示指定学科的老师"""
    try:
        sno = int(request.GET.get('sno', 1))
        print(sno)
        subject = Subject.objects.get(no=sno)
        teachers = subject.teacher_set.all()
        return render(request, 'teachers.html', {'subject': subject, 'teachers': teachers})
    except (KeyError, ValueError, Subject.DoesNotExist):
        return redirect('/')


def praise_or_criticize(request):
    """好评"""
    try:
        print(request)
        tno = int(request.GET['tno'])
        teacher = Teacher.objects.get(no=tno)
        request_path = request.path.split('/')
        # if request.path.startswith('/pr=aise'):
        if 'praise' in request_path:
            teacher.good_count += 1
        else:
            teacher.bad_count += 1
        teacher.save()
        data = {'code': 200, 'hint': 'success'}
    except (KeyError, ValueError, Teacher.DoseNotExist):
        data = {'code': 404, 'hint': 'success'}
    return JsonResponse(data)


def register(request):
    page, hint = 'register.html', ''
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            page = 'login.html'
            hint = '注册成功，请登录'
        else:
            hint = '请输入有效的注册信息'
    return render(request, page, {'hint': hint})


def get_captcha_text(length=4):
    selected_chars = random.choices(ALL_CHARS, k=length)
    return ''.join(selected_chars)


def get_captcha(request):
    """获得验证码"""

    captcha_text = get_captcha_text()
    print(type(request.session))
    request.session['captcha'] = captcha_text
    image = Captcha.instance().generate(captcha_text)
    return HttpResponse(image, content_type='image/png')


def login(request):
    hint = ''
    if request.method == 'POST':
        # 检查浏览器是否支持cookie
        if request.method == 'POST':
            if request.session.test_cookie_worked():
                request.session.delete_test_cookie()

                # login process
                form = LoginForm(request.POST)
                if form.is_valid():
                    # 对验证码的正确性进行验证
                    captcha_from_user = form.cleaned_data['captcha']
                    captcha_from_sess = request.session.get('captcha', '')
                    if captcha_from_sess.lower() != captcha_from_user.lower():
                        hint = '请输入正确的验证码'
                    else:
                        username = form.cleaned_data['username']
                        password = form.cleaned_data['password']
                        user = User.objects.filter(username=username, password=password).first()
                        if user:
                            # 登录成功后将用户编号和用户名保存在session中
                            request.session['userid'] = user.no
                            request.session['username'] = user.username
                            return redirect('/')
                        else:
                            hint = '用户名或密码错误'
                else:
                    hint = '请输入有效的登录信息'
                    
            else:
                return HttpResponse("Please enable cookies and try again.")
        request.session.set_test_cookie()

    return render(request, 'login.html', {'hint': hint})


def logout(request):
    """注销"""
    request.session.flush()
    return redirect('/')
