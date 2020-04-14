from django.shortcuts import render
from create_table import create
from insert_document import insert
from modify_documents import update
from revision_history import getHistory
# Create your views here.
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
# from .serializers import TaskSerializer
# from .models import Task
from constants import Constants
import boto3 
import json
import ast
client = boto3.client('qldb')

@api_view(['GET'])
def apiOverview(request):
    api_urls ={
        'apiOverview':'api/api-overview',
        'createLedger':'api/createledger',
        'createTable':'api/createtable',
        'insertRecords':'api/insertrecords',
        'updateRecords':'api/updaterecords',
        'revisionHistory':'api/gethistory',
        }
    return Response(api_urls)

@api_view(['POST'])
def CreateLedger(request):
    
    data=request.data
    data =data.dict()
    # print(data)
    data=ast.literal_eval(data['data'])
    # print(data)
    # print(type(ast.literal_eval(data)))
    data = ast.literal_eval(data)
    

    
    response = client.create_ledger(
        Name=data['Name'],
        Tags={
            'string': 'string'
        },
        PermissionsMode='ALLOW_ALL',
        DeletionProtection=True
    )
    # # {
    #     "Name":"Rec"
    # # }
    return Response(response)


@api_view(['POST'])
def CreateTable(request):
    # ledgername = request.data['Ledgername']
    # Constants.LEDGERNAME=ledgername
    data=request.data
    data =data.dict()
    data=ast.literal_eval(data['data'])
    data = ast.literal_eval(data)
    
    response = create(data['Tablename'])
    # {
    #     "Ledgername":"Rec",
    #     "Tablename":"Person",
    # }
    return Response(response)


@api_view(['POST'])
def insertRecords(request):
    print(request.data)
    # {
    #     "tablename":tablename,
    #     "data":[
    #         {
    #             "firstname":firstname
    #         },{
    #             "firstname":firstname
    #         }
    #     ]
    # }
    data=request.data
    data =data.dict()
    data=ast.literal_eval(data['data'])
    data = ast.literal_eval(data)
    response = insert(data["tablename"],data["data"])
    return Response(response)

@api_view(['POST'])
def updateRecords(request):
    # print(request.data)
    #  {
    #         "tablename":"Person",
    #         "data":{
    #             "field":"firstname","oldrecord":"qwer","newrecord":"surya"
    #             }
    # }
    # data="{'tablename':'Person','data':{'field':'firstname','oldrecord':'surya','newrecord':'munirathinam'}}"
    
    data=request.data
    data =data.dict()
    data=ast.literal_eval(data['data'])
    data = ast.literal_eval(data)
    response = update(data["tablename"],data["data"])
    return Response(response)

@api_view(['POST'])
def revisionHistory(request):
    # {
    #     "tablename":"Person",
    #     "data":{
    #             "field":"firstname","searchrecord":"muni"
    #             }

    # }
    # data="{'tablename':'person','data':{'field':'firstname','searchrecord':'munirathinam'}}"
    data=request.data
    data =data.dict()
    data=ast.literal_eval(data['data'])
    data = ast.literal_eval(data)
    response = getHistory(data["tablename"],data["data"])
    return Response(response)

