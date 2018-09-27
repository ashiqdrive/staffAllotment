from django.shortcuts import render, render_to_response
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

# Code Done using django-filter dependency
"""from .filters import StaffFilter"""

def staffIndex(request,ttid):
	""" First Show Which Shift to Select """
	shiftList=Shift.objects.all()
	queryset=TimeTable.objects.filter(id=ttid)
	timetableName=queryset.get().longName
	request.session['timetableSession'] = ttid
	request.session['timetableName'] = timetableName
	context={"shiftList":shiftList,}
	return render(request, 'allotment/staff_index.html',context=context)

def staffList(request,pk):
	staffNameList=Staff.objects.filter(department__shift=pk).order_by('dateofJoining')
	context={'staffNameList': staffNameList}
	return render(request, 'allotment/staff_list.html', context=context)

def allotExam(request,pk):
	querysetStaff = Staff.objects.filter(id=pk)
	staffName=querysetStaff.get().name
	timetable_id=request.session['timetableSession']
	examList = Exam.objects.filter(timetable_id=timetable_id)
	context={
	'staffName': staffName,
	'examList': examList,
	}
	return render(request, 'allotment/allot_exam.html', context=context)

class StaffCreate(CreateView):
	model=Staff
	fields = '__all__'
	success_url = reverse_lazy('staff_index')

from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from .forms import SelectExamsForm

def selectExamsForStaffsForATimeTable(request,pk):
	#Getting Staff Name
	querysetStaff = Staff.objects.filter(id=pk)
	staffName = querysetStaff.get().name
	#Get Timetable id from Sessions
	timetable_id = request.session['timetableSession']
	timetableName = request.session['timetableName'] 
	#Exam query Set
	qs = Exam.objects.filter(timetable_id=timetable_id)
	qs2 = Exam.objects.filter(staffs=pk)
	exam_instance = get_object_or_404(Exam, pk=pk)
	#Declaring Form
	form = SelectExamsForm(qs,qs2)
	context = {'form':form, 'staffName':staffName, 'timetableName':timetableName}
	return render_to_response('allotment/exam_form.html', context=context)
	"""# If this is a POST request then process the Form data
#if request.method == 'POST':
Create a form instance and populate it with data from the request (binding):
#form = SelectExamsForm(request.POST)
   
# Else If this is a GET (or any other method) create the default form
else:
form = SelectExamsForm(qs)
return render_to_response('exam_form.html', {'form': form},)"""