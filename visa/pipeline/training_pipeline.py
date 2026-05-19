

from visa.logger import logger
from visa.exception import CustomException
import sys 
from visa.components.data_ingestion import DataIngestion
from visa.components.data_validation import Datavalidation
from visa.components.data_transformation import DataTransformation
from visa.components.model_trainer import ModelTrainer
from visa.components.model_evalutaion import ModelEvaluation

from visa.entity.config_entity import (DataIngestionConfig,
                                       DataValidationConfig,
                                       DataTransformationConfig,
                                       ModelTrainerConfig,
                                       ModelEvaluationConfig)

from visa.entity.artifact_entity import (DataIngestionArtifact,
                                         DataValidationArtifact,
                                         DataTransformationArtifact,
                                         ModelTrainerArtifact,
                                         ModelEvaluationArtifcat)




class TrainingPipeline:

    def __init__(self,Data_Ingestion_Config:DataIngestionConfig,
                 data_validation_config:DataValidationConfig,
                 data_transformation_config:DataTransformationConfig,
                 model_trainer_config:ModelTrainerConfig,
                 Model_evaluation_Config:ModelEvaluationConfig):
        try:

            self.data_ingestion = Data_Ingestion_Config
            self.data_validation = data_validation_config
            self.data_transformation = data_transformation_config
            self.model_trainer_config = model_trainer_config
            self.model_evaluation_config= Model_evaluation_Config
        
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


    def start_data_validation(self,train_file_path,test_file_path)-> DataValidationArtifact:

        try :
            logger.info("Entered into start data validation module in Training Pipeline")

            data_validation = Datavalidation(data_validation=self.data_validation)

            data_validation_status,drift_status,drift_file_path = data_validation.initiate_data_validation(train_file_path=train_file_path,test_file_path=test_file_path)


            data_validation_artifact = DataValidationArtifact(

                validation_status= data_validation_status,
                drift_status= drift_status,
                drift_report_file_path = drift_file_path
    
            )

            return data_validation_artifact

        except  Exception as e:

            raise CustomException(e,sys)

        
    def start_data_transformation(self, data_ingestion_artifact:DataIngestionArtifact,data_validation_artifact:DataValidationArtifact)->DataTransformationArtifact:

        try:

            logger.info("Entered into start data transformation module in training pipeline")

            data_transformation = DataTransformation(
                data_ingestion_artifact=data_ingestion_artifact,
                data_validation_artifact=data_validation_artifact,
                data_transformation_config=self.data_transformation
            )

            data_transformation_artifact = data_transformation.initiate_data_transformation()

            return data_transformation_artifact

        
        except Exception as e:

            raise CustomException(e,sys)
        
    
    def Start_model_training(self,data_transformation_artifact:DataTransformationArtifact)->ModelTrainerArtifact:

        try:

            logger.info("Entered into start  model training module in training pipeline")

            model_trainer_obj = ModelTrainer(model_training_config=self.model_trainer_config,data_transformation_artifact=data_transformation_artifact)

            modeltrained = model_trainer_obj.initiate_model_trainer()

            return modeltrained

        
        except Exception as e:

            raise CustomException(e,sys)
    def start_model_evaluation(self,data_ingetion_artifact:DataIngestionArtifact,
                                      model_trained_artifact:ModelTrainerArtifact)->ModelEvaluationArtifcat:
        
        try :

            logger.info("Entered into start model Evaluation module in training")

            model_evaluation_obj = ModelEvaluation(model_evaluation_config=self.model_evaluation_config,
                                                   model_trained_artifact=model_trained_artifact,
                                                   data_ingestion_artifact=data_ingetion_artifact)
            
            model_evaluation_artifact = model_evaluation_obj.initiate_model_evaluation()

            return model_evaluation_artifact
        

        except Exception as e:

            raise CustomException(e,sys)
        
         

    def run_pipeline(self):

        try :

            data_ingestion_artifact = self.start_data_ingestion()

            data_validation_artifact = self.start_data_validation(train_file_path=data_ingestion_artifact.train_file_path,test_file_path=data_ingestion_artifact.test_file_path)

            data_transformation_artifact = self.start_data_transformation(data_ingestion_artifact=data_ingestion_artifact,data_validation_artifact=data_validation_artifact)

            model_trainer_artifcat = self.Start_model_training(data_transformation_artifact=data_transformation_artifact)

            model_evalution_artifact = self.start_model_evaluation(data_ingetion_artifact=data_ingestion_artifact,model_trained_artifact=model_trainer_artifcat)

        
        except Exception as e:

            raise CustomException(e,sys)
        

    


