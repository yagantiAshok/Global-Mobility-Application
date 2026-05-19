

import sys
from visa.pipeline.training_pipeline import TrainingPipeline
from visa.logger import logger
from visa.exception import CustomException
from visa.entity.config_entity import (DataIngestionConfig,
                                       DataValidationConfig,
                                       DataTransformationConfig,
                                       ModelTrainerConfig,
                                       ModelEvaluationConfig)

try :

    logger.info("Training Pipeline Started ")

    Training_obj = TrainingPipeline(Data_Ingestion_Config=DataIngestionConfig,
                                    data_validation_config=DataValidationConfig,
                                    data_transformation_config=DataTransformationConfig,
                                    model_trainer_config=ModelTrainerConfig,
                                    Model_evaluation_Config=ModelEvaluationConfig)

    start_Training = Training_obj.run_pipeline()

    logger.info("Taining Piepline Over")

except Exception as e:

    raise CustomException(e,sys)