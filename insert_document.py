
from logging import basicConfig, getLogger, INFO

from constants import Constants
from sample_data import convert_object_to_ion, SampleData, get_document_ids_from_dml_results
from connect_to_ledger import create_qldb_session

logger = getLogger(__name__)
basicConfig(level=INFO)



def insert_documents(transaction_executor, table_name, documents):
   
    logger.info('Inserting some documents in the {} table...'.format(table_name))
    statement = 'INSERT INTO {} ?'.format(table_name)
    cursor = transaction_executor.execute_statement(statement, documents)
    list_of_document_ids = get_document_ids_from_dml_results(cursor)

    return list_of_document_ids


    

def insert(table_name,data):
    try:
        with create_qldb_session() as session:
       
            msg=session.execute_lambda(lambda executor: insert_documents(executor,table_name,data),
                                   lambda retry_attempt: logger.info('Retrying due to OCC conflict...'))
            logger.info('Documents inserted successfully!')
    except Exception:
        logger.exception('Error inserting or updating documents.')
    return msg
