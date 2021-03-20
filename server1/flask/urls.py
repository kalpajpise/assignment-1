from django.contrib import admin
from django.urls import path,include

import flask.views as flask_views

urlpatterns = [
    path('search/', flask_views.IFSCSerachView.as_view() , name= "Search IFSC"),
    path('banklead/', flask_views.BankLeadBoardView.as_view(), name= " Bank Lead Board"),
    path('stats/', flask_views.StatisticsView.as_view(), name = "Statictis Details"),
]