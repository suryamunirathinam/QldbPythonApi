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
    response = client.create_ledger(
        Name=request.data['Name'],
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
    response = create(request.data['Tablename'])
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
    response = insert(request.data["tablename"],request.data["data"])
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
    response = update(request.data["tablename"],request.data["data"])
    return Response(response)

@api_view(['POST'])
def revisionHistory(request):
    # {
    #     "tablename":"Person",
    #     "data":{
    #             "field":"firstname","searchrecord":"muni"
    #             }

    # }
    response = getHistory(request.data["tablename"],request.data["data"])
    return Response(response)

