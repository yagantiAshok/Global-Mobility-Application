
import os 
import sys
from visa.logger import logger
from visa.exception import CustomException
from visa.entity.config_entity import DataIngestionConfig
from visa.data_access.visa_data import visaData
from visa.utils.main_utile import create_directories
from pandas import DataFrame
from sklearn.model_selection import train_test_split
import pandas as pd




class DataIngestion:

    def __init__(self,data_ingestion_config:DataIngestionConfig):

        self.data_ingestion_config = data_ingestion_config

        logger.info("we Got data Ingestion Config Deatils In Data Ingestion Class")
    

    def getting_DataFrom_Mongodb(self)->DataFrame:

        try :

            if (os.path.exists(self.data_ingestion_config.data_ingestion_main_dir)):

                logger.info(f"Datsest already Exists at Given Location {self.data_ingestion_config.data_ingestion_main_dir}")

                data_set = pd.read_csv(self.data_ingestion_config.data_ingestion_main_dir)

                return data_set
            
            logger.info("Entered into Getting Data From MongoDb Module ")

            visa_data = visaData()

            data_frame = visa_data.Extracting_Data_From_MongoDB(collection_name=self.data_ingestion_config.Mongo_DB_collection_name)

            logger.info("We converted MongoDb Data into DataFrame")

            # dir name for saving my dataframe 

            # dir_name = os.path.dirname(self.data_ingestion_config.data_ingestion_main_dir)

            create_directories(self.data_ingestion_config.data_ingestion_main_dir)

            data_frame.to_csv(self.data_ingestion_config.data_ingestion_main_dir,index=False,header=True)

            logger.info(f"Data Successfully Stored at {self.data_ingestion_config.data_ingestion_main_dir}")


            return data_frame

        except Exception as e:

            raise CustomException(e,sys)
    
    def split_data_train_test(self,Data_frame):


        try:

            if (os.path.exists(self.data_ingestion_config.training_file_path) and (os.path.exists(self.data_ingestion_config.test_file_path))):

                logger.info("Train and Test data splitted")

                return self.data_ingestion_config.training_file_path,self.data_ingestion_config.test_file_path

            logger.info("Entered into split data train test module")


            train,test = train_test_split(Data_frame, test_size = self.data_ingestion_config.train_test_split_ratio,shuffle=True)

            create_directories(self.data_ingestion_config.training_file_path)

            train.to_csv(self.data_ingestion_config.training_file_path,index=False,header = True)

            test.to_csv(self.data_ingestion_config.test_file_path,index=False,header=True)

            logger.info("Train and Test data successfully stored")

            return self.data_ingestion_config.training_file_path,self.data_ingestion_config.test_file_path

            


        except Exception as e:

            raise CustomException(e,sys)
    
    def Data_ingestion_stage(self):

        try:
           
           logger.info("Entered into Data Ingestion Stage ")

           data_frame = self.getting_DataFrom_Mongodb()

           train_path,test_path = self.split_data_train_test(Data_frame=data_frame)

           return train_path,test_path
        
        except Exception as e:

            raise CustomException(e,sys)
        
        
    
    
