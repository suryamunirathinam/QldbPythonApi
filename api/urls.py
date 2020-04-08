from django.urls import  path 
from . import views


urlpatterns =[
    path('apioverview/',views.apiOverview,name="api-overview"),
    path('createledger/',views.CreateLedger,name="createledger"),
    path('createtable/',views.CreateTable,name="createtable"),
    path('insertrecords/',views.insertRecords,name="insertrecords"),
    path('updaterecords/',views.updateRecords,name="updaterecords"),
    path('gethistory/',views.revisionHistory,name="gethistory"),

    # path('create-ledger/', views.createLedger, name="create-ledger"),
    # path('task-detail/<str:pk>/', views.taskDetail, name="task-detail"),
    # path('task-create/', views.taskCreate, name="task-create"),
    # path('task-update/<str:pk>', views.taskUpdate, name="task-update"),
    # path('task-delete/<str:pk>',views.taskDelete,name="task-delete"),
]