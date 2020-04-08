
from logging import basicConfig, getLogger, INFO

from constants import Constants
from connect_to_ledger import create_qldb_session

logger = getLogger(__name__)
basicConfig(level=INFO)


def create_table(transaction_executor, table_name):
  
    logger.info("Creating the '{}' table...".format(table_name))
    statement = 'CREATE TABLE {}'.format(table_name)
    cursor = transaction_executor.execute_statement(statement)
    logger.info('{} table created successfully.'.format(table_name))
    return len(list(cursor))


def create(table_name):
    try:
        with create_qldb_session() as session:
            session.execute_lambda(lambda x :create_table(x,table_name),lambda retry_attempt: logger.info('Retrying due to OCC conflict...'))                       
                                    
            msg = table_name+' Table created successfully.'
    except Exception:
        msg = 'Error Creating '+ table_name +' table'
    return msg