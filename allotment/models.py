from django.db import models
from django.utils import timezone

class Shift(models.Model):
    name=models.CharField(max_length=25)
    nickName=models.CharField(max_length=30)

    class Meta:
        verbose_name = "Shift"
        verbose_name_plural = "Shifts"
    def __str__(self):
        return f'{self.name}'

class Department(models.Model):
    shift=models.ForeignKey(Shift,on_delete=models.CASCADE)
    name=models.CharField(max_length=100, null=False, blank=False)

    class Meta:
        verbose_name='Department'
        verbose_name_plural='Departments'
    def __str__(self):
        return f'{self.name}'

class Staff(models.Model):
    name=models.CharField(max_length=200, null=False, blank=False)
    department=models.ForeignKey(Department,on_delete=models.CASCADE, null=False, blank=False)
    dateofJoining=models.DateField(null=False, default=timezone.now)
    
    class Meta:
        verbose_name = "Staff"
        verbose_name_plural = "Staffs"
    def __str__(self):
        return f'{self.name}, {self.department}'

class TimeTable(models.Model):
    shortname=models.CharField(max_length=20, help_text='Enter a short name for timetable, this name is not displayed in the report')
    longName=models.CharField(max_length=120, help_text='Enter the TimeTable name which is printed in the final reports')
    oneStaffPer_Students=models.IntegerField(null=False, blank=True, default=0, help_text='Number of students for which one is required, this is used to calculate the no of staffs required for an examination')

    class Meta:
        verbose_name = "TimeTable"
        verbose_name_plural = "TimeTables"
    def __str__(self):
        return f' {self.shortname}'

class Exam(models.Model):
    class Meta:
        unique_together=(('timetable_id','dateOfExam'))
        #Timetable id and exam date is together used as a primary key because a timetable cannot have 2 similar dates its just imposible
        verbose_name = "Exam"
        verbose_name_plural = "Exams"

    timetable_id=models.ForeignKey(TimeTable,on_delete=models.CASCADE, blank=False)
    dateOfExam=models.DateField(null=False, blank=False, default=timezone.now)
    noOfStudents=models.IntegerField(null=False, blank=True, default=0, help_text='No of students appearing for this exam')
    staffs=models.ManyToManyField(Staff, help_text='Select staffs for the exam', blank=True)

    def __str__(self):
        return f' {self.dateOfExam}'