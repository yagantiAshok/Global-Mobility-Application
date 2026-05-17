

import sys
from visa.logger import logger
from visa.exception import CustomException
import numpy as np
import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler,OneHotEncoder,OrdinalEncoder
from sklearn.compose import ColumnTransformer
from visa.constants import SCHEMA_FILE
from datetime import datetime

from visa.entity.config_entity import DataTransformationConfig
from visa.entity.artifact_entity import DataValidationArtifact,DataIngestionArtifact,DataTransformationArtifact

from visa.utils.main_utile import read_yaml,save_object,save_numpy_array

from visa.entity.estimator import TargetValuemapping

class DataTransformation:

    def __init__(self,data_transformation_config:DataTransformationConfig,
                 data_ingestion_artifact:DataIngestionArtifact,
                 data_validation_artifact:DataValidationArtifact):
        try : 

            self.data_transfomation_config = data_transformation_config
            self.data_ingestion_artifact =  data_ingestion_artifact
            self.data_validation_artifact = data_validation_artifact
            self.schema_file = read_yaml(SCHEMA_FILE)
        
        except Exception as e:

            raise CustomException(e,sys)
    
    @staticmethod
    def read_data(file_path)->pd.DataFrame:

        try:

            data = pd.read_csv(file_path)

            return data
        
        except Exception as e:

            raise CustomException(e,sys)
    
    def get_data_transformer_object(self):

        try:

            logger.info("Entered Into get_transformer object")

            logger.info("Intializing objects for Transformation ")


            ordinal_columns = self.schema_file.ordinal_encoding
            onehot_columns = self.schema_file.one_hot_encode
            numerical_columns = self.schema_file.numerical_columns_after_feature_engineering

            logger.info("Got all columns from schema file  ")

            numerical_pipeline = Pipeline(steps=[
                ("imputer", SimpleImputer(strategy="median")),
                ("scaler", StandardScaler())
            ])

            ordinal_pipeline = Pipeline(steps=[
                ("imputer",SimpleImputer(strategy="most_frequent")),
                ("scaler",OrdinalEncoder())
            ])

            one_hot_pipeline = Pipeline(steps=[

                ("imputer", SimpleImputer(strategy="most_frequent")),
                ("sclaer", OneHotEncoder(handle_unknown="ignore"))
            ])


            preprocessor = ColumnTransformer(transformers=[
                ("numerical_columns",numerical_pipeline,numerical_columns),
                ("ordinal_columns",ordinal_pipeline,ordinal_columns),
                ("one_hot_columns",one_hot_pipeline,onehot_columns)
            ])
            

            logger.info("Created preprocessor object for columnTransformer")

            return preprocessor
        
        
        except Exception as e:

            raise CustomException(e,sys)
    

    def initiate_data_transformation(self)->DataTransformationArtifact:

        try :

            if not self.data_validation_artifact.validation_status:

                raise Exception(f"validation Status failed ")

            preprocessor = self.get_data_transformer_object()

            logger.info("Loaded preprocessor Object in initiate_data_transformation module ")

            train_data = DataTransformation.read_data(file_path=self.data_ingestion_artifact.train_file_path)

            test_data  = DataTransformation.read_data(file_path=self.data_ingestion_artifact.test_file_path)

            logger.info("loaded Train and Test data")

            train_input_features = train_data.drop(columns=self.schema_file.Target_Column.Target,axis = 1)

            train_target_feature = train_data[self.schema_file.Target_Column.Target]

            logger.info("Splitted Train Data into independent and dependent features")


            # New column we have year of establishment column that is in year format 
            # converting into  current age

            train_input_features["comapny_age"] = datetime.now().year - train_input_features["yr_of_estab"]

            logger.info("Created new column COMPANY AGE ")

            # removing unwanted columns

            train_input_features = train_input_features.drop(columns=self.schema_file.drop_columns,axis=1)

            logger.info("Columns dropped from Train Set")

            train_target_feature = train_target_feature.replace(TargetValuemapping().__dict__)

            # Now for test data same processs

            test_input_features = test_data.drop(columns = [self.schema_file.Target_Column.Target])

            test_traget_feature = test_data[self.schema_file.Target_Column.Target]

            logger.info("splitted test data into independent and dependent features")

            test_input_features["comapny_age"] = datetime.now().year - test_input_features["yr_of_estab"]

            # now drop columns 

            test_input_features = test_input_features.drop(columns = self.schema_file.drop_columns,axis = 1)

            logger.info("Columns dropped from Test set ")

            test_target_feature = test_traget_feature.replace(TargetValuemapping().__dict__)

            logger.info("transforming train data By using preprocessor object")

            train_input_process_features = preprocessor.fit_transform(train_input_features)

            logger.info("transforming teat data by preprocesor object")

            test_input_process_features = preprocessor.transform(test_input_features)

            
            final_train_array = np.c_[train_input_process_features,np.array(train_target_feature)]

            final_test_array = np.c_[test_input_process_features,np.array(test_target_feature)]

            logger.info("We concated train and test with their target feature")

            # now saving all final results 

            save_object(self.data_transfomation_config.transformed_obj_file_path,preprocessor)
            logger.info(f"saving processor object at {self.data_transfomation_config.transformed_obj_file_path}")

            save_numpy_array(self.data_transfomation_config.transformed_train_file_path,final_train_array)
            logger.info(f"train data saving at {self.data_transfomation_config.transformed_train_file_path}")

            save_numpy_array(self.data_transfomation_config.transformed_test_file_path,final_test_array)
            logger.info(f"test data saved at {self.data_transfomation_config.transformed_test_file_path}")


            data_transformation_artifact = DataTransformationArtifact(
                transformed_obj_file_path= self.data_transfomation_config.transformed_obj_file_path,
                transformed_train_file_path=self.data_transfomation_config.transformed_train_file_path,
                transformed_test_file_path= self.data_transfomation_config.transformed_test_file_path
            )

            return data_transformation_artifact


        
        except Exception as e:

            raise CustomException(e,sys)