from dbconfig import read_db_config
from pymongo import MongoClient
 
 
def connect():
    """ Connect to MySQL database """
 

    db_config = read_db_config()
    host = db_config['host']
    user = db_config['user']
    password = db_config['password']
    database = db_config['database']

    client = MongoClient(host)
    client.tempdb.authenticate(user, password, mechanism='SCRAM-SHA-1')

    return client.tempdb