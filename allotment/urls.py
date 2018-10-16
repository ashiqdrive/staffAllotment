from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('timetable/', views.TimeTableList.as_view(), name='timetableList'),
]

# Add URLConf to create, update, and delete TimeTable
urlpatterns += [  
    path('timetable/create/', views.TimeTableCreate.as_view(), name = 'timetable_create'),
    path('timetable/<int:pk>/update/', views.TimeTableUpdate.as_view(), name = 'timetable_update'),
    path('timetable/<int:pk>/delete/', views.TimeTableDelete.as_view(), name = 'timetable_delete'),
    path('timetable/<int:pk>/detail/', views.timetable_detail, name = 'timetable_detail'),
    #----- New  Implementation 16 - OCT - 2018 ------------
    path('timetable/<int:ttid>/', views.timetableDetailedView, name = 'timetableDetailedView'),
    path('timetable/<int:ttid>/addexam/', views.AddExam.as_view(), name = 'add_exam'),
    path('timetable/<int:ttid>/exam/<int:exid>/delete/', views.DelExam.as_view(), name = 'del_exam'),
]

urlpatterns += [
    path('exam/create', views.ExamCreate.as_view(), name='exam_create'),
    path('exam/<int:pk>/delete/', views.ExamDelete.as_view(), name='exam_delete'),
    path('exam/<int:pk>/edit/', views.ExamEdit.as_view(), name='exam_edit'),
    path('exam/<int:pk>/allotstaff/', views.ExamAllotStaff.as_view(), name='exam_allotstaff'),
    path('exam/<int:pk>/report/', views.report, name='report'),
]

#Report
urlpatterns+=[
    path('report/', views.report, name='report'),
    #path('reportbystaff/', views.report, name='report_by_staff'),
    #path('reportbyexam/', views.report, name='report-by_exam'),
]