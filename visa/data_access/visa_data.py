



from visa.logger import logger
from visa.exception import CustomException
import sys
import pandas as pd
from visa.configuration.mongo_db_connection import MongoDBclient
from visa.constants import DATA_BASE_NAME
from typing import Optional


class visaData:

    def __init__(self):

        try:
           
           self.mongo_client = MongoDBclient(data_base_name=DATA_BASE_NAME)

        except Exception as e:
            raise CustomException(e,sys)
    
    def Extracting_Data_From_MongoDB(self,collection_name, database_name:Optional[str] = None)->pd.DataFrame:
        try:
            
            if database_name is None: 

                collection = self.mongo_client.data_base[collection_name]
            else:

                collection = self.mongo_client.client[database_name][collection_name]

            logger.info("We got collection From MongoDB")

            data_frame = pd.DataFrame(list(collection.find()))

            return data_frame

        except Exception as e:

            raise CustomException(e,sys)
        pass