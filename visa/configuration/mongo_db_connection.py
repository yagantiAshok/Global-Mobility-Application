

from visa.logger import logger
from visa.exception import CustomException
import sys
import os
from visa.constants import MONGODB_URL_KEY

import pymongo
import certifi

ca = certifi.where()

class MongoDBclient:

    client = None

    def __init__(self,data_base_name):
        
        try:
            if MongoDBclient.client is None:

                mongo_db_url_key = os.getenv(MONGODB_URL_KEY)

                if mongo_db_url_key is None:

                    raise Exception(f"Environment Key not Existed : {MONGODB_URL_KEY}")
                
                MongoDBclient.client = pymongo.MongoClient(mongo_db_url_key,tlsCAFile=ca)
        
            self.client = MongoDBclient.client

            self.data_base = self.client[data_base_name]

            logger.info("MONGODBC ONNECTION SUCCESSFULL")

        except Exception as e:
            raise CustomException(e,sys)
            