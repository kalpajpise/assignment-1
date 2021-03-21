from django.contrib import admin
from django.urls import path , include
from . import views

urlpatterns = [
    path('search/', views.IFSCSearchView.as_view() , name= "Search IFSC"),
    path('banklead/', views.BankLeadBoardView.as_view(), name= " Bank Lead Board"),
    path('stats/', views.StatisticsView.as_view(), name = "Statictis Details")
]
