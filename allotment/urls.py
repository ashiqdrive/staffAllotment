from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('timetable/', views.TimeTableList.as_view(), name='timetableList'),
    path('staff/<int:ttid>', views.staffIndex, name='staff_index'),
]

# Add URLConf to create, update, and delete TimeTable
urlpatterns += [  
    path('timetable/create/', views.TimeTableCreate.as_view(), name='timetable_create'),
    path('timetable/<int:pk>/update/', views.TimeTableUpdate.as_view(), name='timetable_update'),
    path('timetable/<int:pk>/delete/', views.TimeTableDelete.as_view(), name='timetable_delete'),
    path('timetable/<int:pk>/detail/', views.timetable_detail, name='timetable_detail'),
]

urlpatterns += [
    path('exam/create', views.ExamCreate.as_view(), name='exam_create'),
    path('exam/<int:pk>/delete/', views.ExamDelete.as_view(), name='exam_delete')
]

urlpatterns += [  
    path('staff/create/', views.StaffCreate.as_view(), name='staff_create'),
    path('staff/<int:pk>/list/', views.staffList, name='staff_list'),# This is Shift Id
    path('staff/<int:pk>/allotexam/', views.selectExamsForStaffsForATimeTable, name='allot_exam'), #  This is Staff id 
    #path('staff/<int:pk>/update/', views.StaffUpdate.as_view(), name='staff_update'),
    #path('staff/<int:pk>/delete/', views.StaffDelete.as_view(), name='staff_delete'),
    #path('staff/<int:pk>/detail/', views.staff_detail, name='staff_detail'),
]
