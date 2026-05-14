


import os 
from datetime import datetime
from visa.constants import *
from dataclasses import dataclass


TIMESTAMP = datetime.now().strftime("%m_%d_%Y_%M_%H_%S")


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

