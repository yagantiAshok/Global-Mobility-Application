

import sys
from visa.exception import CustomException
from visa.logger import logger

from visa.components.data_ingestion import DataIngestion

from visa.entity.config_entity import DataIngestionConfig
from visa.entity.artifact_entity import DataIngestionArtifact

class TrainingPipeline:

    def __init__(self,data_ingestion:DataIngestionConfig=DataIngestionConfig):

        try :
            self.data_ingestion_config = data_ingestion
        except Exception as e:
            raise CustomException(e,sys)
        pass
    
    def start_data_ingestion(self)->DataIngestionArtifact:

        try:

            logger.info("Entered into start data ingestion method of training pipeline")

            data_ingestion = DataIngestion(data_ingestion_config=self.data_ingestion_config)

            data_ingestion_artifact = data_ingestion.initiate_data_ingestion()

            logger.info("Got train and test data from MongoDB")

            return data_ingestion_artifact
        
        except Exception as e:
            raise  CustomException(e,sys)
        
    def run_pipeline(self):

        try:

            data_ingestion_artifact = self.start_data_ingestion()

        except Exception as e:

            raise CustomException(e,sys)



