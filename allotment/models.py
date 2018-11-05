from django.db import models
from django.utils import timezone
from django.urls import reverse

class Shift(models.Model):
    name=models.CharField(max_length=25)
    nickName=models.CharField(max_length=30)

    class Meta:
        verbose_name = "Shift"
        verbose_name_plural = "Shifts"
    def __str__(self):
        return f'{self.name}'
    def get_go_to_staff_list_url(self):
        return reverse('staff_list', args=[str(self.id)])

class Department(models.Model):
    shift=models.ForeignKey(Shift,on_delete=models.CASCADE)
    name=models.CharField(max_length=100, null=False, blank=False)

    class Meta:
        verbose_name='Department'
        verbose_name_plural='Departments'
    def __str__(self):
        return f'{self.name}, {self.shift}'

from datetime import date
from dateutil.relativedelta import relativedelta

class Staff(models.Model):
    name=models.CharField(max_length=200, null=False, blank=False)
    department=models.ForeignKey(Department,on_delete=models.CASCADE, null=False, blank=False)
    dateofJoining=models.DateField(null=False, default=timezone.now)
    exams=models.ManyToManyField('Exam', help_text='Select Exams for the staffs', blank=True)
    class Meta:
        verbose_name = "Staff"
        verbose_name_plural = "Staffs"
    def __str__(self):
        return f'{self.name}'
    def get_absolute_url(self):
        return reverse('allot_exam', args=[str(self.id)])
    def get_no_of_days(self):
        today = date.today()
        doj = self.dateofJoining
        return (today-doj).days
    def get_years_of_experience(self):
        today = date.today()
        doj = self.dateofJoining
        #experienceInYears = relativedelta(today, doj)
        diff = ((today-doj).days)/365
        return diff

class TimeTable(models.Model):
    shortname=models.CharField(max_length=20, help_text='Enter a short name for timetable, this name is not displayed in the report')
    longName=models.CharField(max_length=120, help_text='Enter the TimeTable name which is printed in the final reports')
    oneStaffPer_Students=models.IntegerField(null=False, blank=True, default=0, help_text='Number of students for which one is required, this is used to calculate the no of staffs required for an examination')

    class Meta:
        verbose_name = "TimeTable"
        verbose_name_plural = "TimeTables"
    def __str__(self):
        return f' {self.shortname}'
    def get_update_url(self):
        return reverse('timetable_update', args=[str(self.id)])
    def get_delete_url(self):
        return reverse('timetable_delete', args=[str(self.id)])
    def get_details_url(self):
        return reverse ('timetable_detail', args=[str(self.id)])
    def get_detailedView_url(self):
        return reverse ('timetableDetailedView', args=[str(self.id)])
    def get_allot_staff_url(self):
        return reverse ('staff_index', args=[str(self.id)])

class Exam(models.Model):
    class Meta:
        unique_together=(('dateOfExam','session'))
        #Timetable id and exam date is together used as a primary key because a timetable cannot have 2 similar dates its just imposible
        verbose_name = "Exam"
        verbose_name_plural = "Exams"

    timetable_id=models.ForeignKey(TimeTable,on_delete=models.CASCADE,blank=False)
    dateOfExam=models.DateField(null=False, blank=False, default=timezone.now)
    noOfStudents=models.IntegerField(null=False, blank=True, default=0, help_text='No of students appearing for this exam')
    session=models.ForeignKey('Session',on_delete=models.CASCADE,blank=False,default=1)
    #staffs=models.ManyToManyField(Staff, help_text='Select staffs for the exam', blank=True)

    def get_delete_url(self):
        return reverse('exam_delete', args=[str(self.id)])

    #def get_exam_allotstaff_url(self):
        #return reverse('exam_allotstaff', args=[str(self.id)])

    def get_edit_url(self):
        return reverse('exam_edit', args=[str(self.id)])
        
    def get_report_url(self):
        return reverse('report', args=[str(self.id)])

    def get_staff_count(self):
        return Staff.objects.filter(exams=self).count()
    
    def get_no_of_staffs_needed(self):
        oneStaffPer = TimeTable.objects.filter(id=self.timetable_id_id).get().oneStaffPer_Students
        staffsRequired=self.noOfStudents/oneStaffPer
        return int(staffsRequired)
    
    def __str__(self):
        formatedDate = self.dateOfExam.strftime("%d-%m-%y, %a")
        return f' {formatedDate},{self.session.shortName}'

class Session(models.Model):

    class Meta:
        verbose_name = "Session"
        verbose_name_plural = "Sessions"

    name = models.CharField(max_length=20, null=False, blank=False)
    shortName = models.CharField(max_length=4, null=False, blank=False)

    def __str__(self):
        return f' {self.name}'
    