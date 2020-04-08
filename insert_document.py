
from logging import basicConfig, getLogger, INFO

from constants import Constants
from sample_data import convert_object_to_ion, SampleData, get_document_ids_from_dml_results
from connect_to_ledger import create_qldb_session

logger = getLogger(__name__)
basicConfig(level=INFO)


def update_person_id(document_ids):

    
    new_land_registrations = SampleData.LAND_REGISTRATION.copy()
    for i in range(len(SampleData.PERSON)):
        
        registration = new_land_registrations[i]
        
        registration['Owners'].update({'PersonId': str(document_ids[i])})
    return  new_land_registrations


def insert_documents(transaction_executor, table_name, documents):
   
    logger.info('Inserting some documents in the {} table...'.format(table_name))
    statement = 'INSERT INTO {} ?'.format(table_name)
    cursor = transaction_executor.execute_statement(statement, documents)
    list_of_document_ids = get_document_ids_from_dml_results(cursor)

    return list_of_document_ids


# def update_and_insert_documents(transaction_executor,table_name,data):
   
#     list_ids = insert_documents(transaction_executor, Constants.PERSON_TABLE_NAME, SampleData.PERSON)

#     logger.info("Records for the table "+ table_name +)
#     new_registrations = update_person_id(list_ids)

#     insert_documents(transaction_executor, Constants.LAND_TABLE_NAME, SampleData.LAND)
#     insert_documents(transaction_executor, Constants.LAND_REGISTRATION_TABLE_NAME, new_registrations)
    

def insert(table_name,data):
    try:
        with create_qldb_session() as session:
       
            msg=session.execute_lambda(lambda executor: insert_documents(executor,table_name,data),
                                   lambda retry_attempt: logger.info('Retrying due to OCC conflict...'))
            logger.info('Documents inserted successfully!')
    except Exception:
        logger.exception('Error inserting or updating documents.')
    return msg
