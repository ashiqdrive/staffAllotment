from django.shortcuts import render

from .models import Shift, Department, Staff, TimeTable, Exam

def index(request):
	"""View Function of Home Page"""
	StaffListCount=Staff.objects.count()
	StaffNamesList=Staff.objects.filter(department__shift=1).order_by('name')

	context={
	'StaffListCount':StaffListCount,
	'StaffNamesList':StaffNamesList
	}

	return render(request,'index.html', context=context)

from django.views import generic

class TimeTableList(generic.ListView):
	model = TimeTable

from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

class TimeTableCreate(CreateView):
	model=TimeTable
	fields = '__all__'
	success_url = reverse_lazy('timetableList')

class TimeTableUpdate(UpdateView):
	model=TimeTable
	fields = '__all__'
	success_url = reverse_lazy('timetableList')

class TimeTableDelete(DeleteView):
	model=TimeTable
	success_url = reverse_lazy('timetableList')
#_____________________________________________________

def timetable_detail(request, pk):
	#View function for listing exam dates related to a specfic timetable
	queryset1=TimeTable.objects.filter(id=pk)
	timetableName=queryset1.get().longName
	examDateList=Exam.objects.filter(timetable_id=pk).order_by('dateOfExam')
	context={
	'examDateList':examDateList,
	'timetableName':timetableName,
	'pk':pk
	}
	return render(request,'allotment/timetable_detail.html',context=context)

from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from .forms import AddExams
def add_exam(request, pk):
	#Method to show form to add exams in a particular timetable
	exam = Exam

	# If this is a POST request then process the Form data
	if request.method == 'POST':
		# Create a form instance and populate it with data from the request (binding):
		form = AddExams(request.POST)
		#check is the form is valid
		if form.is_valid():
			# process the data in form.cleaned_data as required (here we just write it to the model due_back field)
			exam.timetable_id = form.cleaned_data['timetable']
			exam.dateOfExam = form.cleaned_data['dateOfExam']
			exam.noOfStudents = form.cleaned_data['noOfStudents']
			exam.save()
		return HttpResponseRedirect(reverse('timetable_detail') )
	# If this is a GET (or any other method) create the default form
	else:
		timetable_id = pk
		form = AddExams(initial={'timetable': timetable_id,})
		return render(request, 'allotment/add_exam_form.html', {'form': form, 'exam':exam})