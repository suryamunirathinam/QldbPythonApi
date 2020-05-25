from django.urls import  path 
from . import views


urlpatterns =[
    path('apioverview/',views.apiOverview,name="api-overview"),
    path('createledger/',views.CreateLedger,name="createledger"),
    path('createtable/',views.CreateTable,name="createtable"),
    path('insertrecords/',views.insertRecords,name="insertrecords"),
    path('updaterecords/',views.updateRecords,name="updaterecords"),
    path('gethistory/',views.revisionHistory,name="gethistory"),

   
]