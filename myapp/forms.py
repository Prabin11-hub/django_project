from django import forms
from django.contrib.auth.models import User
from .models import Student, Teacher, Result,Course


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ['username', 'email', 'password']

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['full_name', 'roll_number']

class TeacherForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = ['full_name', 'subject_speciality']


class ResultForm(forms.ModelForm):
    class Meta:
        model = Result
        fields = ['student', 'course', 'marks_obtained']

    def _init_(self, teacher=None, *args, **kwargs):
        super(ResultForm, self)._init_(*args, **kwargs)
        if teacher:
            self.fields['course'].queryset = Course.objects.filter(teacher=teacher)
            self.fields['student'].queryset = Student.objects.filter(courses__teacher=teacher).distinct()




class ResultSearchForm(forms.Form):
    course = forms.ModelChoiceField(queryset=Course.objects.none(), label="Select Course")

    def _init_(self, student, *args, **kwargs):
        super(ResultSearchForm, self)._init_(*args, **kwargs)
        self.fields['course'].queryset = student.courses.all()