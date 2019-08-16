from django.shortcuts import render, redirect
from django.http import JsonResponse
from vote.models import Subject, Teacher


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
