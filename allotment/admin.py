from django.contrib import admin
from .models import Shift, Department, Staff, TimeTable, Exam, Session
# Register your models here.
admin.site.register(Shift)
admin.site.register(Department)
#admin.site.register(Staff)
admin.site.register(TimeTable)
admin.site.register(Exam)
admin.site.register(Session)

@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    fields = ['name', 'department','dateofJoining','exams']
    list_display = ('name', 'department')
    list_filter = ['department']
