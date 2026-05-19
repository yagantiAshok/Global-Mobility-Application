

from visa.entity.config_entity import ModelEvaluationConfig
from visa.entity.artifact_entity import ModelTrainerArtifact,DataIngestionArtifact,ModelEvaluationArtifcat
from sklearn.metrics import f1_score
from visa.exception import CustomException
from typing import Optional
from visa.logger import logger
from datetime import datetime
import sys
import pandas as pd
from dataclasses import dataclass
from visa.entity.estimator import TargetValuemapping,visamodel
from visa.entity.s3_estimator import VisaEstimator
from visa.constants import TARGET_COLUMN

@dataclass
class EvaluateModelRespone:
    trained_model_f1_score : float
    best_model_f1_score: float
    is_model_accepted: None
    difference : float


class ModelEvaluation:

    def __init__(self,model_evaluation_config:ModelEvaluationConfig,
                      model_trained_artifact:ModelTrainerArtifact,
                      data_ingestion_artifact:DataIngestionArtifact):
        
        self.model_evalution_config = model_evaluation_config
        self.mode_trained_artifact = model_trained_artifact
        self.data_ingestion_artifact = data_ingestion_artifact
    
    def get_best_model(self) ->Optional[visamodel]:

        try:

            bucket_name = self.model_evalution_config.bucket_name
            model_path = self.model_evalution_config.s3_model_path

            visa_model = VisaEstimator(bucket_name=bucket_name,model_path=model_path)

            if visa_model.is_model_present(model_path=model_path):
                
                return visa_model
            
            return None
        
        except Exception as e:

            raise CustomException(e,sys)
    
    def evaluate_model(self)->EvaluateModelRespone:

        try:

            logger.info("Entered into evaluate model module in modelevaluation")

            test_df = pd.read_csv(self.data_ingestion_artifact.test_file_path)

            test_df["comapny_age"] = datetime.now().year - test_df["yr_of_estab"]

            x,y = test_df.drop(columns=[TARGET_COLUMN],axis = 1), test_df[TARGET_COLUMN]

            y = y.replace(
                TargetValuemapping().__dict__
            )
            
            trained_model_f1_score = self.mode_trained_artifact.metric.f1_score

            best_model_f1_score = None

            best_model = self.get_best_model()

            if best_model is not None:

                y_hat_best_model = best_model.predict(x)

                best_model_f1_score= f1_score(y,y_hat_best_model)

            tmp_best_model_score = 0 if best_model_f1_score is None else best_model_f1_score

            result = EvaluateModelRespone(
                trained_model_f1_score=trained_model_f1_score,
                best_model_f1_score=best_model_f1_score,
                is_model_accepted=trained_model_f1_score>tmp_best_model_score,
                difference=trained_model_f1_score-tmp_best_model_score
            )
            logger.info(f"result {result}")

            return result


        except Exception as e:
            raise CustomException(e,sys)
    
    def initiate_model_evaluation(self)->ModelEvaluationArtifcat:

        try:

            logger.info("entered into initiate model evaluation")

            evaluate_model_evalution = self.evaluate_model()
            s3_model_path = self.model_evalution_config.s3_model_path

            model_evaluation_artifact = ModelEvaluationArtifcat(
                is_model_accepted=evaluate_model_evalution.is_model_accepted,
                s3_model_path=s3_model_path,
                trained_model_path=self.mode_trained_artifact.trained_model_path,
                changed_accuracy=evaluate_model_evalution.difference
            )

            logger.info("Got model Evaluation artiofact ")

            return model_evaluation_artifact

        
        except Exception as e:

            raise CustomException(e,sys)
