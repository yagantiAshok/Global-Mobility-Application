
import os
import sys
from visa.exception import CustomException
from visa.logger import logger
from visa.constants import DATA_BASE_NAME,MONGODB_URL_KEY
import pymongo

import certifi
ca = certifi.where()
class MongoDBClient:

    client = None

    def __init__(self,data_base_name = DATA_BASE_NAME):

        try:

            if MongoDBClient.client is None:
                mongo_db_url = os.getenv(MONGODB_URL_KEY)

                if mongo_db_url is None:

                    raise Exception(f"Environment Key {MONGODB_URL_KEY} not present ")
                
                MongoDBClient.client = pymongo.MongoClient(mongo_db_url,tlsCAFile=ca)
            
            self.client = MongoDBClient.client

            self.database  = self.client[data_base_name]

            logger.info("MongoDBconnnection successfully")
        except Exception as e:
            raise CustomException(e,sys)


                

            