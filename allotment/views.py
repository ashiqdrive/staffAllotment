from django.shortcuts import render

from .models import Shift, Department, Staff, TimeTable

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

class timetableList(generic.ListView):
	#Generic Class Based List view for Timetable
	model = TimeTable
