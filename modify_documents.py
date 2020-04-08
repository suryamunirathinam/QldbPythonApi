
from logging import basicConfig, getLogger, INFO

from sample_data import get_document_ids, print_result, SampleData
from constants import Constants
from sample_data import convert_object_to_ion
from connect_to_ledger import create_qldb_session

logger = getLogger(__name__)
basicConfig(level=INFO)




def updateinfo(transaction_executor,tablename,data):
   
    
    statement = "UPDATE {} AS r SET r.{} ='{}' WHERE r.{}= '{}'".format(tablename,data['field'],data['newrecord'],data['field'],data['oldrecord'])
    print(statement)
        # updata tablename as r set r.firstname = "surya" where r.firstname = "qwer"
    cursor = transaction_executor.execute_statement(statement)
    print(cursor)
    try:
        print_result(cursor)
        # logger.info('Successfully updated info  to new owner.'.format())
    except StopIteration:
        raise RuntimeError('Unable to transfer vehicle, could not find registration.')
    return cursor




def update(tablename,data):
    print(tablename)
    print()
    print(data['newrecord'])
    # print(data.field)
    try:
        with create_qldb_session() as session:
    
            session.execute_lambda(lambda executor:updateinfo(executor,tablename,data),
                                lambda retry_attempt: logger.info('Retrying due to OCC conflict...'))
            
            msg="updated info"
    except Exception:
        logger.exception('error in updation ')
        msg= 'error'
    return msg
       
# {
#             "tablename":"Person",
#             "data":{
#                 "field":"firstname","oldrecord":"qwer","newrecord":"surya"
#                 }
#     }