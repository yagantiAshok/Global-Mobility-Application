


import os 
from datetime import datetime
from visa.constants import *
from dataclasses import dataclass


TIMESTAMP = datetime.now().strftime("%m_%d_%Y_%H_%M_%S")


@dataclass
class TrainingPipelineConfig:

    artifact: str = os.path.join("Artifact",TIMESTAMP)


trainingpipelineConfig: TrainingPipelineConfig = TrainingPipelineConfig()


@dataclass
class DataIngestionConfig:

    data_ingestion_dir_name : str = os.path.join(trainingpipelineConfig.artifact,DATA_INGESTION_DIR)
    data_ingestion_main_dir : str = os.path.join(data_ingestion_dir_name,DATA_INGESTION_MAIN_DATA_DIR,DATA_SET_NAME)
    data_ingestion_ingested_dir :str = os.path.join(data_ingestion_dir_name,DATA_INGESTION_INGESTED_DIR)
    training_file_path : str = os.path.join(data_ingestion_dir_name,DATA_INGESTION_INGESTED_DIR,TRAIN_DATASET_NAME)
    test_file_path :str = os.path.join(data_ingestion_dir_name,DATA_INGESTION_INGESTED_DIR,TEST_DATASET_NAME)
    train_test_split_ratio :float = DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO
    Mongo_DB_collection_name : str = DATA_INGESTION_COLLECTION_NAME



@dataclass
class DataValidationConfig:

    data_validation_dir_name :str = os.path.join(trainingpipelineConfig.artifact,DATA_VALDATION_DIR)
    data_validation_drift_file_path: str = os.path.join(data_validation_dir_name,DATA_VAIDATION_DRIFT_DIR,DATA_VALIDATION_DRIFT_FILE_NAME)
    data_validation_status_path : str = os.path.join(data_validation_dir_name,DATA_VALIDATION_STATUS_DIR,DATA_VALIDATION_STATUS_FILE)
    
@dataclass

class DataTransformationConfig:

    data_transformation_dir :str = os.path.join(trainingpipelineConfig.artifact,DATA_TRANSFORMATION_DIR)

    transformed_train_file_path: str = os.path.join(data_transformation_dir,DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR,
                                                    TRAIN_DATASET_NAME.replace("csv","npy"))
    
    transformed_test_file_path: str = os.path.join(data_transformation_dir,DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR,
                                                   TEST_DATASET_NAME.replace("csv","npy"))
    
    transformed_obj_file_path: str = os.path.join(data_transformation_dir,DATA_TRANSFORMATION_TRANSFORMED_OBJECT_DIR,PROCESSING_OBJ_FILE_NAME)

@dataclass

class ModelTrainerConfig:

    model_trainer_dir :str = os.path.join(trainingpipelineConfig.artifact,MODEL_TRAINER_DIR)
    modle_trianed_file_path: str = os.path.join(model_trainer_dir,MODEL_TRAINER_TRAINED_DIR,MODEL_TRAINER_TRAINED_MODEL_NAME)
    model_excepted_score: float = MODEL_TRAINER_EXPECTED_SCORE
    model_config_file_path :str = MODEL_TRAINER_MODEL_CONFIG_FILE_PATH

