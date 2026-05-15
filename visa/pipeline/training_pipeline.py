

from visa.logger import logger
from visa.exception import CustomException
import sys 
from visa.components.data_ingestion import DataIngestion
from visa.components.data_validation import Datavalidation
from visa.entity.config_entity import DataIngestionConfig,DataValidationConfig
from visa.entity.artifact_entity import DataIngestionArtifact,DataValidationArtifact




class TrainingPipeline:

    def __init__(self,Data_Ingestion_Config:DataIngestionConfig,data_validation_config:DataValidationConfig):
        try:

            self.data_ingestion = Data_Ingestion_Config
            self.data_validation = data_validation_config
        
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
        

    def start_data_validation(self,test_path)-> DataValidationArtifact:

        try :
            logger.info("Entered into start data validation module in Training Pipeline")

            data_validation = Datavalidation(data_validation=self.data_validation)

            validation  = data_validation.validating_testset_columns(test_data_path=test_path)

            data_validation_artifact = DataValidationArtifact(
                validation_status = validation
            )

            return data_validation_artifact

        except  Exception as e:

            raise CustomException(e,sys)
         

    def run_pipeline(self):

        try :

            data_ingestion_artifact = self.start_data_ingestion()

            data_validation_artifact = self.start_data_validation(data_ingestion_artifact.test_file_path)
        
        except Exception as e:

            raise CustomException(e,sys)
        

    


