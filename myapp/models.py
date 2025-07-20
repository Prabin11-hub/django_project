from django.db import models
from django.contrib.auth.models import User

class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    subject_speciality = models.CharField(max_length=100)

    def __str__(self):
        return self.full_name


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    roll_number = models.CharField(max_length=50, unique=True)
    grade = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.full_name} ({self.roll_number})"


class Course(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20)
    teacher = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True, related_name='courses')

    def __str__(self):
        return f"{self.name} ({self.code})"


class Result(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='results')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='results')
    marks_obtained = models.IntegerField()

    class Meta:
        unique_together = ('student', 'course')

    def __str__(self):
        return f"{self.student.full_name} - {self.course.name}: {self.marks_obtained}"
