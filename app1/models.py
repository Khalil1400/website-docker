from django.db import models

# Create your models here.


class Student(models.Model):
    Student_id= models.IntegerField(primary_key=True)
    Student_name = models.CharField(max_length=30)
    gpa = models.IntegerField(default=0)


class Course_Taken(models.Model):
    Student_id=models.ForeignKey(Student,on_delete=models.CASCADE)
    Course_id= models.IntegerField()
    Semester=models.CharField(max_length=100)
    Number_of_credits= models.IntegerField()
    Grade = models.IntegerField()