from django.shortcuts import render, render_to_response
from .models import Shift, Department, Staff, TimeTable, Exam
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from django.forms.models import modelform_factory
from django import forms


def index(request):
	"""View Function of Home Page"""
	StaffListCount=Staff.objects.count()
	StaffNamesList=Staff.objects.filter(department__shift=1).order_by('name')

	return render(request,'index.html')

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

# New Detailed View of TimeTable
def timetableDetailedView(request, ttid):
	queryset=TimeTable.objects.filter(id=ttid)
	timetableName=queryset.get().longName
	examDateList=Exam.objects.filter(timetable_id=ttid).order_by('dateOfExam')
	context={
	'examDateList':examDateList,
	'timetableName':timetableName,
	'ttid':ttid,
	}
	#request.session['timetableSession'] = ttid
	#request.session['timetableName'] = timetableName
	return render(request,'allotment/timetable_detail.html',context=context)

# Class based Generic Create View to create and Add New Exam for a particular timetable
class AddExam(CreateView):
	model = Exam
	fields=['timetable_id','dateOfExam','session']
	HEADING="Add Exams"
	template_name = 'allotment/add_exam.html'

	def get_context_data(self, **kwargs): #Code to sent context to templete
		ctx = super(AddExam,self).get_context_data(**kwargs)
		ctx['HEADING'] = self.HEADING 
		return ctx

	def get_initial(self): # Code to set initial values in the form
		ttid = self.kwargs['ttid'] # code to get the parameter from url
		return { 'timetable_id':ttid }

	def get_success_url(self):
		ttid = self.kwargs['ttid'] # code to get the parameter from url 
		return reverse_lazy('timetableDetailedView',args=[str(ttid)])

# Class Based generic Delete View to Delete a Exam belonging to a particular timetable
class DelExam(DeleteView):
	model = Exam
	pk_url_kwarg = 'exid'

	def get_context_data(self, **kwargs):
		ctx = super(DelExam,self).get_context_data(**kwargs)
		ttid = self.kwargs['ttid'] # code to get the parameter from url 
		queryset=TimeTable.objects.filter(id=ttid)
		timetableName=queryset.get().longName
		ctx['timetableName'] = timetableName
		return ctx

	def get_success_url(self):
		ttid = self.kwargs['ttid'] # code to get the parameter from url 
		return reverse_lazy('timetableDetailedView',args=[str(ttid)])

def confirmDelete(request):
	text = "Are you sure you want to reset the timetable data this willl delete all the exam dates and staffs alloted for the timetable"
	return render(request, 'allotment/confirm_delete_all_exams.html')

from django.http import HttpResponseRedirect

def deleteAllExams(request):
	queryset = Exam.objects.all().delete()
	#return HttpResponseRedirect('')
	return render(request, 'allotment/delete_sucess.html')

# Method to Select Shift to Allot Staff
def selectShift(request,ttid,exid):
	queryset=Shift.objects.all()
	ttid = ttid
	exid = exid
	context = {
	'ttid':ttid,
	'exid':exid,
	'shiftList':queryset,
	}
	return render(request,'allotment/select_shift.html', context=context)

#Method to select shift to allot duty
def allotDuty_SelectShift(request,ttid):
	queryset=Shift.objects.all()
	ttid = ttid
	context = {
	'ttid':ttid,
	'shiftList':queryset,
	}
	return render(request,'allotment/allot_duty_select_shift.html', context=context)

#Method to display Staff List by Shift
def allotDuty_Staff_List_by_Shift(request,ttid,shiftid):
	queryset = Staff.objects.all().filter(department__shift = shiftid).order_by('-dateofJoining')
	shiftName = Shift.objects.get(id=shiftid)
	ttid = ttid
	shiftid = shiftid
	context = {
	'ttid': ttid,
	'staffByShiftList': queryset,
	'shiftid' : shiftid
	}
	return render(request,'allotment/allotDuty_staff_list_by_shift.html', context=context)

#Main method to Allot duty for staffs i.e to select exams for staffs
class AllotDutyMain(UpdateView):
	""" Used to select Exams for Staffs based on a Timetable id"""
	model = Staff
	pk_url_kwarg = 'staffid'

	#fields = ['name','department','exams']

	form_class =  modelform_factory(Staff,fields=['id','name','department','exams'],
		widgets={"exams": forms.CheckboxSelectMultiple()})

	def get_form(self, form_class=form_class):
		ttid = self.kwargs['ttid'] # code to get the parameter from url 
		form = super(AllotDutyMain,self).get_form(form_class) #instantiate using parent
		form.fields['exams'].queryset = Exam.objects.all().filter(timetable_id = ttid).order_by('dateOfExam')
		return form

	def get_success_url(self):
		ttid = self.kwargs['ttid'] # code to get the parameter from url
		shiftid = self.kwargs['shiftid']
		return reverse_lazy('allotDuty_Staff_List_by_Shift',kwargs={ 'ttid': ttid, 'shiftid':shiftid })

class AllotStaffForExam(UpdateView):
	pass
"""class AllotStaffForExam(UpdateView):
	Used to select staff names with a multi choice tick box
	model = Exam
	pk_url_kwarg = 'exid'

	form_class =  modelform_factory(Exam,fields=['timetable_id','dateOfExam','noOfStudents'],#'staffs'
		widgets={"staffs": forms.CheckboxSelectMultiple()})

	def get_form(self, form_class=form_class):
		shid = self.kwargs['shid'] # code to get the parameter from url 
		form = super(AllotStaffForExam,self).get_form(form_class) #instantiate using parent
		#form.fields['staffs'].queryset = Staff.objects.all().filter(department__shift=shid).order_by('-dateofJoining')
		form.fields['timetable_id'].disabled=True
		form.fields['dateOfExam'].disabled=True
		form.fields['noOfStudents'].disabled=True
		return form

	def get_success_url(self):
		ttid = self.kwargs['ttid'] # code to get the parameter from url 
		return reverse_lazy('timetableDetailedView',args=[str(ttid)])"""



"""class ExamEdit(UpdateView):
	#Used to Edit no of students attending for this exam
	model = Exam
	form_class =  modelform_factory(Exam,fields=['timetable_id','dateOfExam','noOfStudents'])
	def get_form(self, form_class=form_class):
		form = super(ExamEdit,self).get_form(form_class) #instantiate using parent
		form.fields['timetable_id'].disabled=True
		form.fields['dateOfExam'].disabled=True
		return form
	def get_success_url(self):
		timetable_id=self.request.session['timetableSession']
		return reverse_lazy('timetable_detail',args=[str(timetable_id)])"""

def reportByExam(request,ttid,exid):
	queryset=Staff.objects.filter(exams__id=exid)
	timetableName = TimeTable.objects.filter(id = ttid).get().longName
	dateOfExam = Exam.objects.filter(id = exid).get().dateOfExam
	examName = Exam.objects.filter(id = exid).get()
	#session = Exam.objects.filter(id = exid).get().session
	ttid = ttid
	exid = exid
	context = {
	'ttid':ttid,
	'exid':exid,
	'staffList':queryset,
	'timetableName':timetableName,
	'dateOfExam':dateOfExam,
	'examName':examName
	}
	return render(request,'allotment/report_by_exam.html', context=context)

def reportByStaff(request,ttid):
	staffList = Staff.objects.filter(exams__timetable_id=ttid).distinct().order_by('department__shift','department')
	qset = Staff.objects.values('id', 'exams__timetable_id', 'exams__dateOfExam', 'exams__session__name').order_by('exams__dateOfExam')
	timetableName = TimeTable.objects.filter(id = ttid).get().longName
	ttid = ttid
	context = {
	'ttid':ttid,
	'staffList':staffList,
	'timetableName':timetableName,
	'qset':qset,
	}
	return render(request,'allotment/report_by_staffs.html', context=context)


"""def selectExamsForStaffsForATimeTable(request,pk):
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

	# If this is a POST request then process the Form data
	if request.method == 'POST':
		form = SelectExamsForm(request.POST)

		# Check if the form is valid:
		if form.is_valid():
			# process the data in form.cleaned_data as required (here we just write it to the model due_back field)
			examdates = form.cleaned_data['Exams']
			for e in examdates:
				e.staffs.add(pk)
				e.save()
			# redirect to a new URL:
			return HttpResponseRedirect(reverse('staff_list') )
	else:
		#Declaring Form
		form = SelectExamsForm(qs,qs2)
		context = {'form':form, 'staffName':staffName, 'timetableName':timetableName}
	return render_to_response('allotment/exam_form.html', context=context)"""

import io
from django.http import FileResponse
from reportlab.pdfgen import canvas
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.units import inch

def report(request,pk):
	
	queryset=Staff.objects.filter(exam__id=pk)	
	# Create the HttpResponse object with the appropriate PDF headers.
	response = HttpResponse(content_type='application/pdf')
	response['Content-Disposition'] = 'attachment; filename=somefilename.pdf'

	c = canvas.Canvas(response)
	c.setPageSize(A4)
	c.setFont("Helvetica", 14)

	i=5 #Horizontal
	j=750 #Vertical
	a=790
	k=250 #Horizontal
	c.drawString(i,a,"Name")
	c.drawString(k,a,"Department")
	for s in queryset:
		staffName = str(s.name)
		department = str(s.department)
		c.drawString(i,j,staffName)
		c.drawString(k,j,department)
		j=j-20
	c.showPage()
	c.save()
	return response

#Method to select shift
def staffReport(request):
	queryset=Shift.objects.all()
	context = {
	'shiftList':queryset,
	}
	return render(request,'allotment/staff_report_select_shift.html', context=context)


def staffReportMain(request,shiftid):
	queryset = Staff.objects.all().filter(department__shift = shiftid).order_by('-dateofJoining')
	shiftName = Shift.objects.get(id=shiftid)
	shiftid = shiftid
	context = {
	'staffByShiftList': queryset,
	'shiftid' : shiftid
	}
	return render(request,'allotment/staff_report_main.html', context=context)