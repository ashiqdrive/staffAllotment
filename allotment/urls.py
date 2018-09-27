from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('timetable/', views.TimeTableList.as_view(), name='timetableList'),
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