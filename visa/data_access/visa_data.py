
import sys
from visa.logger import logger
from visa.exception import CustomException
import pandas as pd
from pandas import DataFrame
from visa.constants import DATA_BASE_NAME
from visa.configuration.mongo_db_connection import MongoDBClient
from typing import Optional


class VisaData:

    def __init__(self):

        try :

           self.mongo_client = MongoDBClient(data_base_name=DATA_BASE_NAME)

        except Exception as e:
            
            raise CustomException(e,sys)
    
    def export_collection_from_mongo_db(self,collection_name,database_name:Optional[str]=None)->pd.DataFrame:

        try:

            if database_name is None:

                collection = self.mongo_client.database[collection_name]
            else:
                collection = self.mongo_client[database_name][collection_name]

            df = pd.DataFrame(list(collection.find()))

            return df 

        except Exception as e:
            raise CustomException(e,sys)


        