

import os
import sys
from pandas import DataFrame
from sklearn.model_selection import train_test_split
from visa.entity.config_entity import DataIngestionConfig
from visa.entity.artifact_entity import DataIngestionArtifact
from visa.logger import logger
from visa.exception import CustomException
from visa.data_access.visa_data import VisaData


class DataIngestion:

    def __init__(self,data_ingestion_config:DataIngestionConfig=DataIngestionConfig()):

        try :
            self.data_ingestion_config = data_ingestion_config

        except Exception as e:

            raise CustomException(e,sys)
        
    
    def exporting_data_into_feature_store(self)->DataFrame:

        try:

            logger.info("Exporting Data from mongodb")

            us_visadata = VisaData()

            dataframe = us_visadata.export_collection_from_mongo_db(collection_name= self.data_ingestion_config.data_ingestion_collection_name)
            
            logger.info(f"shape of data {dataframe.shape}")

            feature_store_file_path = self.data_ingestion_config.feature_store_path

            dir_path = os.path.dirname(feature_store_file_path)
            os.makedirs(dir_path,exist_ok=True)

            logger.info(f"saving exported dat in to {feature_store_file_path}")

            dataframe.to_csv(feature_store_file_path,index=False,header=True)

            return dataframe
        
        except Exception as e:
            raise CustomException(e,sys)
    

    def split_data_train_test(self,dataframe:DataFrame):

        try:

            logger.info("Entered into split data as train test module")

            train_set,text_set = train_test_split(dataframe,test_size=self.data_ingestion_config.data_ingestion_train_test_split,shuffle=True)

            logger.info("Completed splitting of DataFrame ")

            dir_path = os.path.dirname(self.data_ingestion_config.training_file_path)

            os.makedirs(dir_path,exist_ok=True)

            train_set.to_csv(self.data_ingestion_config.training_file_path,index=False,header=True)

            text_set.to_csv(self.data_ingestion_config.test_file_path,index=False,header=True)

            logger.info("Exported train test file paths ")

        except Exception as e:
            raise CustomException(e,sys)
        

    def initiate_data_ingestion(self):

        try :

            logger.info("Entered into initiate Data Ingestion phase ")

            dataframe = self.exporting_data_into_feature_store()

            logger.info("Got data from mongodb")

            self.split_data_train_test(dataframe=dataframe)

            logger.info("Perfomed train test split on DataSet")
        
        except Exception as e:

            raise CustomException(e,sys)

    
        







    
