from django.forms import ModelForm
from .models import Student,Course_Taken
from django import forms

# Create the form class.
class CreateStudentForm(ModelForm):
	class Meta:
		model = Student
		fields = ['Student_id', 'Student_name', 'gpa']
# Create the form class.
class CreateCourseForm(ModelForm):
	def clean_Number_of_credits(self):
		credits = self.cleaned_data['Number_of_credits']
		if credits <= 0:
			raise forms.ValidationError('Credits must be greater than zero.')
		return credits

	class Meta:
		model = Course_Taken
		fields = ['Student_id', 'Course_id', 'Semester','Number_of_credits','Grade']

class GPAForm(forms.Form):
	Student_id = forms.IntegerField()
