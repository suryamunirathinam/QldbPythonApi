from datetime import datetime
from decimal import Decimal
from logging import basicConfig, getLogger, INFO

from amazon.ion.simple_types import IonPyBool, IonPyBytes, IonPyDecimal, IonPyDict, IonPyFloat, IonPyInt, IonPyList, \
    IonPyNull, IonPySymbol, IonPyText, IonPyTimestamp
from amazon.ion.simpleion import dumps, loads

logger = getLogger(__name__)
basicConfig(level=INFO)
IonValue = (IonPyBool, IonPyBytes, IonPyDecimal, IonPyDict, IonPyFloat, IonPyInt, IonPyList, IonPyNull, IonPySymbol,
            IonPyText, IonPyTimestamp)


class SampleData:

    
    PERSON = [
        {
            'FirstName': 'Raul',
            'LastName': 'Lewis',
            'Address': '1719 University Street, Seattle, WA, 98109',
            'DOB': datetime(1963, 8, 19),
            'GovId': '1111 2222 3333',
            'GovIdType': 'Aadhaar'
        },
        {
            'FirstName': 'Brent',
            'LastName': 'Logan',
            'DOB': datetime(1967, 7, 3),
            'Address': '43 Stockert Hollow Road, Everett, WA, 98203',
            'GovId': '2222 3333 4444',
            'GovIdType': 'Aadhaar'
        },
        {
            'FirstName': 'Alexis',
            'LastName': 'Pena',
            'DOB': datetime(1974, 2, 10),
            'Address': '4058 Melrose Street, Spokane Valley, WA, 99206',
            'GovId': '3333 4444 5555',
            'GovIdType': 'Aadhaar'
        },
        {
            'FirstName': 'Melvin',
            'LastName': 'Parker',
            'DOB': datetime(1976, 5, 22),
            'Address': '4362 Ryder Avenue, Seattle, WA, 98101',
            'GovId': '4444 5555 6666',
            'GovIdType': 'Aadhaar'
        },
        {
            'FirstName': 'Salvatore',
            'LastName': 'Spencer',
            'DOB': datetime(1997, 11, 15),
            'Address': '4450 Honeysuckle Lane, Seattle, WA, 98101',
            'GovId': '5555 6666 7777',
            'GovIdType': 'Aadhaar'
        }
    ]
    LAND = [
        {
            'SurveyNO': '1N4AL11D75C109151',
            'Type': 'Agri',
            'Sq_feet':1000
        },
        {
            'SurveyNO': 'KM8SRDHF6EU074761',
            'Type': 'Agri',
            'Sq_feet':1000
        },
        {
            'SurveyNO': '3HGGK5G53FM761765',
            'Type': 'Flat',
            'Sq_feet':1000
        },
        {
            'SurveyNO': '1HVBBAANXWH544237',
            'Type': 'Flat',
            'Sq_feet':1000
        },
        {
            'SurveyNO': '1C4RJFAG0FC625797',
            'Type': 'Commertial',
            'Sq_feet':1000
        }
    ]
    LAND_REGISTRATION = [
        {
            'SurveyNO': '1N4AL11D75C109151',
            'LandRegNo': 'LEWISR261LL',
            'State': 'WA',
            'City': 'Seattle',
            
            'MarketValue': 50000,
            'Owners': {
                'PersonId':''}
                
            
        },
        {
            'SurveyNO': 'KM8SRDHF6EU074761',
            'LandRegNo': 'CA762X',
            'State': 'WA',
            'City': 'Kent',
            'MarketValue': 50000,
            
            'Owners': {
                'PersonId': ''}
        },
        {
            'SurveyNO': '3HGGK5G53FM761765',
            'LandRegNo': 'CD820Z',
            'State': 'WA',
            'City': 'Everett',
            'MarketValue': 50000,
            'Owners': {
                'PersonId': ''}
        },
        {
            'SurveyNO': '1HVBBAANXWH544237',
            'LandRegNo': 'LS477D',
            'State': 'WA',
            'City': 'Tacoma',
            'MarketValue': 50000,
            
            'Owners': {
                'PersonId': ''}
                
            
        },
        {
            'SurveyNO': '1C4RJFAG0FC625797',
            'LandRegNo': 'TH393F',
            'State': 'WA',
            'City': 'Olympia',
            'MarketValue': 50000,

            'Owners': {
                'PersonId': ''}
        }
    ]


def convert_object_to_ion(py_object):

    ion_object = loads(dumps(py_object))
    return ion_object


def to_ion_struct(key, value):
 
    ion_struct = dict()
    ion_struct[key] = value
    return loads(str(ion_struct))


def get_document_ids(transaction_executor,value):
    
    query ="SELECT metadata.id FROM _ql_committed_Person AS p where p.data.GovId ='{}'".format(value)
    # query = "SELECT id FROM {} AS t BY id WHERE t.{} = '{}'".format(table_name, field, value)
    print(query)
    cursor = transaction_executor.execute_statement(query)
    print(cursor)
    list_of_ids = list(map(lambda table: table.get('id'), cursor))
    print(list_of_ids)
    return list_of_ids


def get_document_ids_from_dml_results(result):
   
    ret_val = list(map(lambda x: x.get('documentId'), result))
    return ret_val


def print_result(cursor):
   
    result_counter = 0
    for row in cursor:
        
        logger.info(dumps(row, binary=False, indent='  ', omit_version_marker=True))
        result_counter += 1
    return result_counter