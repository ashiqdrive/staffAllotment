from django.shortcuts import render
from .models import Shift, Department, Staff, TimeTable, Exam
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy


def index(request):
	"""View Function of Home Page"""
	StaffListCount=Staff.objects.count()
	StaffNamesList=Staff.objects.filter(department__shift=1).order_by('name')

	context={
	'StaffListCount':StaffListCount,
	'StaffNamesList':StaffNamesList
	}
	return render(request,'index.html', context=context)

#____________________
#_____TimeTable _____

class TimeTableList(generic.ListView):
	model = TimeTable

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
	queryset1=TimeTable.objects.filter(id=pk)
	timetableName=queryset1.get().longName
	examDateList=Exam.objects.filter(timetable_id=pk).order_by('dateOfExam')
	context={
	'examDateList':examDateList,
	'timetableName':timetableName,
	'pk':pk,
	}
	request.session['timetableSession'] = pk
	request.session['timetableName'] = timetableName
	return render(request,'allotment/timetable_detail.html',context=context)

#_____________________
#_______ Exam ________
class ExamCreate(CreateView):
	model=Exam
	fields=['timetable_id','dateOfExam','noOfStudents']
	HEADING="Add Exams"
	def get_initial(self):
		timetable_id=self.request.session['timetableSession']
		return { 'timetable_id':timetable_id }
	def get_context_data(self, **kwargs):
		ctx = super(ExamCreate,self).get_context_data(**kwargs)
		ctx['HEADING'] = self.HEADING
		return ctx
	def get_success_url(self):
		timetable_id=self.request.session['timetableSession']
		return reverse_lazy('timetable_detail',args=[str(timetable_id)])

class ExamDelete(DeleteView):
	model = Exam

	def get_context_data(self, **kwargs):
		ctx = super(ExamDelete,self).get_context_data(**kwargs)
		ctx['timetableName'] = self.request.session['timetableName']
		return ctx

	def get_success_url(self):
		timetable_id=self.request.session['timetableSession']
		return reverse_lazy('timetable_detail',args=[str(timetable_id)])

#____________________
#_______ Staff ______

#def staffIndex(request):
	#return render(request,'allotment/staff_index.html')

class StaffCreate(CreateView):
	model=Staff
	fields = '__all__'
	success_url = reverse_lazy('staff_index')

from .filters import StaffFilter
def staffList(request):
	staff_list = Staff.objects.all()
	staff_filter = StaffFilter(request.GET, queryset=staff_list)
	return render(request, 'allotment/staff_list.html', {'filter': staff_filter})
