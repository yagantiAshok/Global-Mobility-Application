
import sys
import numpy as np
import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score,f1_score,precision_score,recall_score
from neuro_mf import ModelFactory
from visa.exception import CustomException
from visa.logger import logger
from visa.utils.main_utile import load_object,read_yaml,save_object,load_numpy_array
from visa.entity.config_entity import ModelTrainerConfig
from visa.entity.artifact_entity import DataTransformationArtifact,ModelTrainerArtifact,ClassificationMetrics
from visa.entity.estimator import visamodel

class ModelTrainer:

    def __init__(self,model_training_config:ModelTrainerConfig,
                 data_transformation_artifact:DataTransformationArtifact):
        
        self.model_trainer_config = model_training_config
        self.data_tarnsformation_artifact = data_transformation_artifact
    

    def get_model_obj_and_report(self,train:np.array,test:np.array):

        try:

            logger.info("Entered into get_modle_obj_and_report module")

            model_factory = ModelFactory(model_config_path=self.model_trainer_config.model_config_file_path)

            x_train,y_train,x_test,y_test = train[:,:-1],train[:,-1],test[:,:-1],test[:,-1]

            logger.info("Dividing into train and Test sets")

            best_model_deatils = model_factory.get_best_model(
                X=x_train,y=y_train,base_accuracy=self.model_trainer_config.model_excepted_score

            )

            logger.info("Got best model details ")

            model_obj = best_model_deatils.best_model

            y_pred = model_obj.predict(x_test)

            f1 = f1_score(y_test,y_pred)
            precision = precision_score(y_test,y_pred)
            recall = recall_score(y_test,y_pred)

            metric_artifact = ClassificationMetrics(
                f1_score=f1,
                precision=precision,
                recall=recall
            )

            logger.info("updated classmetricsArtifact")

            return best_model_deatils,metric_artifact

        except Exception as e:

            raise CustomException(e,sys)
        
    def initiate_model_trainer(self)->ModelTrainerArtifact:

        try:

            logger.info("entered into initiate model trainer module")

            train_arr = load_numpy_array(self.data_tarnsformation_artifact.transformed_train_file_path)
            test_arr = load_numpy_array(self.data_tarnsformation_artifact.transformed_test_file_path)

            best_model,metric_artifact = self.get_model_obj_and_report(train=train_arr,test=test_arr)

            preprocessing_obj = load_object(self.data_tarnsformation_artifact.transformed_obj_file_path)

            if best_model.best_score < self.model_trainer_config.model_excepted_score:

                logger.info("Best model accuracy less then expected score")

                raise Exception("Best model accuracy less then expected score")
            
            visa_model = visamodel(preprocessing_obj=preprocessing_obj,trained_model_obj=best_model.best_model)

            logger.info("created visa_model object with preprocessor and mdoel")

            save_object(self.model_trainer_config.modle_trianed_file_path,visa_model)

            model_trainer_artifact = ModelTrainerArtifact(
                trained_model_path=self.model_trainer_config.modle_trianed_file_path,
                metric= metric_artifact
            )

            logger.info(f"ModelTrainerArtifact {model_trainer_artifact}")

            return model_trainer_artifact

        
        except Exception as e:
            raise CustomException(e,sys)

