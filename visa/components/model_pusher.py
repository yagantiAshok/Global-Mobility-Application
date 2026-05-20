




import sys
from visa.exception import CustomException
from visa.logger import logger
from visa.cloud_storage.aws_storage import SimpleStorageService
from visa.entity.config_entity import ModelPusherConfig
from visa.entity.artifact_entity import ModelPusherArtifact,ModelEvaluationArtifcat
from visa.entity.s3_estimator import VisaEstimator


class ModelPusher:

    def __init__(self,model_evaluation_artifact:ModelEvaluationArtifcat,
                 model_pusher_config:ModelPusherConfig):
        
        self.s3 = SimpleStorageService()

        self.model_evaluation_artifact = model_evaluation_artifact
        self.model_pusher_config = model_pusher_config
        self.visa_estimator = VisaEstimator(bucket_name=model_pusher_config.bucket_name,
                                            model_path=model_pusher_config.s3_model_key_path)
        
    def initiate_model_pusher(self)->ModelPusherArtifact:

        try:

            logger.info("Entered into initiate model pusher method")

            self.visa_estimator.save_model(from_file=self.model_evaluation_artifact.trained_model_path)

            model_pusher_artifact = ModelPusherArtifact(
                bucket_name=self.model_pusher_config.bucket_name,
                s3_model_key_path=self.model_pusher_config.s3_model_key_path
            )

            return model_pusher_artifact

        except Exception as e:

            raise CustomException(e,sys)
