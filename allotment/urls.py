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
    path('timetable/<int:ttid>/exam/<int:exid>/allotstaff/', views.selectShift, name = 'select_shift_to_allot_staff'),
    path('timetable/<int:ttid>/exam/<int:exid>/allotstaff/shift/<int:shid>/', views.AllotStaffForExam.as_view(), name = 'allot_staff'),
    path('timetable/<int:ttid>/exam/<int:exid>/reportbyexam/', views.reportByExam, name = 'reportbyexam'),
    path('timetable/<int:ttid>/reportbystaff/', views.reportByStaff, name = 'reportbystaff'),
]

# 
# ---- New Implementation Urls to allot duty for staffs --- NEW 23 - OCT - 2018 ----- 
urlpatterns += [ 
    path('timetable/resetexam', views.deleteAllExams, name='deleteAllExams'),
    path('timetable/confirmdelete', views.confirmDelete, name='confirmdelete'),
    path('timetable/<int:ttid>/allotduty/', views.allotDuty_SelectShift, name='allotDuty_SelectShift'),
    path('timetable/<int:ttid>/allotduty/shift/<int:shiftid>/', views.allotDuty_Staff_List_by_Shift, name='allotDuty_Staff_List_by_Shift'),
    path('timetable/<int:ttid>/allotduty/shift/<int:shiftid>/staff/<int:staffid>/', views.AllotDutyMain.as_view(), name='allotDutyMain'),
]

urlpatterns += [
    #path('exam/create', views.ExamCreate.as_view(), name='exam_create'),
    #path('exam/<int:pk>/delete/', views.ExamDelete.as_view(), name='exam_delete'),
    #path('exam/<int:pk>/edit/', views.ExamEdit.as_view(), name='exam_edit'),
    #path('exam/<int:pk>/allotstaff/', views.ExamAllotStaff.as_view(), name='exam_allotstaff'),
    #path('exam/<int:pk>/report/', views.report, name='report'),
]

#Report
urlpatterns+=[
    path('report/', views.report, name='report'),
    #path('reportbystaff/', views.report, name='report_by_staff'),
    #path('reportbyexam/', views.report, name='report-by_exam'),
]

urlpatterns+=[
    path('staffreport/', views.staffReport, name='staffReport'),
    path('staffreport/<int:shiftid>', views.staffReportMain, name='staffReportMain'),
]

