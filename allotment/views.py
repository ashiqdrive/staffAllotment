from django.shortcuts import render

from .models import Shift, Department, Staff, TimeTable, Exam

primarykey= 1

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

def timetable_detail(request, pk):

	request.session['timetableSession'] = pk

	queryset1=TimeTable.objects.filter(id=pk)
	timetableName=queryset1.get().longName
	examDateList=Exam.objects.filter(timetable_id=pk).order_by('dateOfExam')
	context={
	'examDateList':examDateList,
	'timetableName':timetableName,
	'pk':pk,
	}
	return render(request,'allotment/timetable_detail.html',context=context)

class ExamCreate(CreateView):
	model=Exam
	fields=['timetable_id','dateOfExam','noOfStudents']

	def get_initial(self):
		timetable_id=self.request.session['timetableSession']
		return {
			'timetable_id':timetable_id
		}
	success_url = reverse_lazy('timetable_detail',args=[str(self.request.session['timetableSession'])])