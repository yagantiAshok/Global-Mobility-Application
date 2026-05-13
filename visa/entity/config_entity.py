
import os 

from visa.constants import *
from dataclasses import dataclass
from datetime import datetime


TIMESTAP :str = datetime.now().strftime("%m_%d_%Y_%H_%M_%S")

@dataclass

class TrainingPipelineConfig:

    piepline: str = PIPELINE_NAME
    artifact :str = os.path.join(ARTIFACT_DIR,TIMESTAP)
    timestap : str = TIMESTAP

trainingpipelineconfig : TrainingPipelineConfig = TrainingPipelineConfig()

@dataclass
class DataIngestionConfig:
    data_ingestion_collection_name :str = DATA_INGESTION_COLLECTION_NAME
    data_ingestion_train_test_split :float = DATA_INGESTION_TRAIN_TEST_SPLIT
    data_ingestion_dir_name :str = os.path.join(trainingpipelineconfig.artifact,DATA_INGESTION_DIR_NAME)
    feature_store_path :str = os.path.join(data_ingestion_dir_name,DATA_INGESTION_FEATURE_STORE_DIR,DATA_SET_NAME)
    training_file_path: str = os.path.join(data_ingestion_dir_name,DATA_INGESTION_INGESTED_DIR,TRAIN_FILE_NAME)
    test_file_path : str = os.path.join(data_ingestion_dir_name,DATA_INGESTION_INGESTED_DIR,TEST_FILE_NAME)  




