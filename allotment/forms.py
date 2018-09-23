from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
    
from django import forms

class AddExams(forms.Form):
	"""
	Form to add Exams for a particular Timetable
	"""
	timetable = forms.IntegerField(editable = False)
	dateOfExam = forms.DateField(help_text="Add exam date for this timetable")
	noOfStudents= froms.IntegerField(help_text="how many students are going to write this exam", blank=True, default=0)
	