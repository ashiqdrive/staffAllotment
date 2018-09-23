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
]

urlpatterns += [
    path('timetable/<int:pk>/detail/', views.timetable_detail, name='timetable_detail'),
]

urlpatterns += [
    path('timetable/<int:pk>/addexam/', views.add_exam, name='add_exam'),
]