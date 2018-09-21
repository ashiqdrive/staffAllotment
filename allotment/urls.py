from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('timetable/', views.timetableList.as_view(), name='timetableList'),
]