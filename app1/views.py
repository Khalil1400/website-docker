from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST
from .forms import CreateStudentForm, CreateCourseForm, GPAForm
from .models import Student, Course_Taken


def update_gpa(student_id):
    courses = Course_Taken.objects.filter(Student_id_id=student_id)
    credits = sum(course.Number_of_credits for course in courses)
    total = sum(course.Grade * course.Number_of_credits for course in courses)
    Student.objects.filter(pk=student_id).update(gpa=total / credits if credits else 0)


@require_POST
def delete_student(request, student_id):
    get_object_or_404(Student, pk=student_id).delete()
    return redirect('add_student')


@require_POST
def delete_course(request, course_id):
    course = get_object_or_404(Course_Taken, pk=course_id)
    student_id = course.Student_id_id
    course.delete()
    update_gpa(student_id)
    return redirect('add_course')


def index(request):
    return render(request, 'index.html')


def add_student(request):
    form = CreateStudentForm(request.POST if request.method == 'POST' else None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('index')
    return render(request, 'add_student.html', {'form': form, 'S': Student.objects.all()})


def add_course(request):
    form = CreateCourseForm(request.POST if request.method == 'POST' else None)
    if request.method == 'POST' and form.is_valid():
        course = form.save()
        update_gpa(course.Student_id_id)
        return redirect('index')
    return render(request, 'add_course.html', {'form': form, 'S': Course_Taken.objects.all()})


def report(request):
    form = GPAForm(request.POST if request.method == 'POST' else None)
    student = None
    if request.method == 'POST' and form.is_valid():
        student = Student.objects.filter(pk=form.cleaned_data['Student_id']).first()
        if student is None:
            form.add_error('Student_id', 'No student with this ID was found.')
    return render(request, 'report_student.html', {'form': form, 'A': student})
