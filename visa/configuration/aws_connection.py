
import boto3
import os

from visa.constants import AWS_ACCESS_KEY_ID_ENV_KEY,AWS_SECRET_ACCESS_KEY_ENV_KEY,REGION_NAME


class S3Client:

    s3_client = None
    s3_resources = None

    def __init__(self,region_name = REGION_NAME):

        if S3Client.s3_resources==None or S3Client.s3_client==None:

            access_key_id = os.getenv(AWS_ACCESS_KEY_ID_ENV_KEY)
            secret_access_key = os.getenv(AWS_SECRET_ACCESS_KEY_ENV_KEY)

            if access_key_id is None:

                raise Exception(f"Environment variable {AWS_ACCESS_KEY_ID_ENV_KEY} is not set")
            
            if secret_access_key is None:

                raise Exception(f"Environment variablle {AWS_SECRET_ACCESS_KEY_ENV_KEY} is not set")
            
            S3Client.s3_resources = boto3.resource('s3',
                                            aws_access_key_id = access_key_id,
                                            aws_secret_access_key = secret_access_key,
                                            region_name = region_name)
            S3Client.s3_client = boto3.client('s3',
                                              aws_access_key_id = access_key_id,
                                              aws_secret_access_key = secret_access_key,
                                              region_name = region_name)
        self.s3_resources = S3Client.s3_resources
        self.s3_client = S3Client.s3_client

