


from dataclasses import dataclass

@dataclass
class DataIngestionArtifact:

    train_file_path : str
    test_file_path : str

@dataclass
class DataValidationArtifact:
    validation_status: bool
    drift_status: str 
    drift_report_file_path :str

@dataclass
class DataTransformationArtifact:
    transformed_obj_file_path: str
    transformed_train_file_path: str
    transformed_test_file_path: str

@dataclass
class ClassificationMetrics:
    f1_score:float
    precision:float
    recall:float

@dataclass

class ModelTrainerArtifact:

    trained_model_path:str
    metric: ClassificationMetrics


@dataclass
class ModelEvaluationArtifcat:
    is_model_accepted : bool
    changed_accuracy :float
    s3_model_path: str
    trained_model_path :str


@dataclass
class ModelPusherArtifact:
    bucket_name :str
    s3_model_key_path: str