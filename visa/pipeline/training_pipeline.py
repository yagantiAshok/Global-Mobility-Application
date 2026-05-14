

from visa.logger import logger
from visa.exception import CustomException
import sys 
from visa.components.data_ingestion import DataIngestion
from visa.entity.config_entity import DataIngestionConfig
from visa.entity.artifact_entity import DataIngestionArtifact




class TrainingPipeline:

    def __init__(self,Data_Ingestion_Config:DataIngestionConfig):

        try:

            self.data_ingestion = Data_Ingestion_Config
        
        except Exception as e:
           
           raise CustomException(e,sys)
        

    def start_data_ingestion(self)->DataIngestionArtifact:

        try:
            
            data_ingestion = DataIngestion(data_ingestion_config=self.data_ingestion)

            train,test = data_ingestion.Data_ingestion_stage()

            Data_Ingestion_artifact = DataIngestionArtifact(

                train_file_path= train,
                test_file_path= test
                
            )

            return Data_Ingestion_artifact


        except  Exception as e:

            raise CustomException(e,sys)
        

    def run_pipeline(self):

        try :

            data_ingestion = self.start_data_ingestion()
        
        except Exception as e:

            raise CustomException(e,sys)
        
    


