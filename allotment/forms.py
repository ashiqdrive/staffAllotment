from django import forms
from .models import Staff, Exam, Shift

class SelectExamsForm(forms.Form):
	def __init__(self, qs=None, *args, **kwargs):
		super(SelectExamsForm, self).__init__(*args, **kwargs)
		if qs:
			self.fields['Exams'] = forms.ModelMultipleChoiceField(
				queryset=qs, widget=forms.CheckboxSelectMultiple())
