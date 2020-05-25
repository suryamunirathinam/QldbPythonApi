from datetime import datetime, timedelta
from logging import basicConfig, getLogger, INFO

from sample_data import print_result, get_document_ids, SampleData
from constants import Constants
from connect_to_ledger import create_qldb_session

logger = getLogger(__name__)
basicConfig(level=INFO)



def docHistory(transaction_executor, tablename,data):
 
   
    # query= "select h.metadata,q.data.FirstName,q.data.LastName from history(LandRegistration) as h inner join _ql_committed_Person as q on h.data.Owners.PersonId=q.metadata.id where h.data.SurveyNO='{}'".format(surveyno)
    query = "select q.metadata.id from History({}) as q Where q.data.{} = '{}'".format(tablename,data['field'],data['searchrecord'])
    cursor = transaction_executor.execute_statement(query)
    result= list(map(lambda table:table.get('id'),cursor))

    query1 = "select q.data.{},q.metadata.version from History({}) as q Where q.metadata.id = '{}'".format(data['field'],tablename,result[0])
    cursor1 = transaction_executor.execute_statement(query1)
    result= list(map(lambda table:{"firstname":table.get('firstname'),"version":table.get('version')},cursor1))
    print(result)
    history_dict ={
        "tablename":tablename,
        "revisions":result
       
    }
    return history_dict
        

def getHistory(tablename,data):
    
    try:
        with create_qldb_session() as session:
            
            res = session.execute_lambda(lambda lambda_executor: docHistory(lambda_executor,tablename,data),
                                   lambda retry_attempt: logger.info('Retrying due to OCC conflict...'))
            logger.info('Successfully queried history.')
    except Exception:
        res ='Unable to query history to find previous owners.'
    return res