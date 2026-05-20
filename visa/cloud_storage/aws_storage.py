

import boto3
from io import StringIO
from typing import Union,List
import os,sys
from visa.exception import CustomException
from visa.logger import logger
from mypy_boto3_s3.service_resource import Bucket
from botocore.exceptions import ClientError
from pandas import DataFrame,read_csv
import pickle
from visa.configuration.aws_connection import S3Client


class SimpleStorageService:

    def __init__(self):

        s3_client = S3Client()
        self.s3_resorces = s3_client.s3_resources
        self.s3_client = s3_client.s3_client
    
    def get_bucket(self,bucket_name)->Bucket:

        logger.info("Entered into getbucket method")

        try:

            bucket = self.s3_resorces.Bucket(bucket_name)
            logger.info("Got the Bucket")

            return bucket
        
        except Exception as e:

            raise CustomException(e,sys)



    
    def s3_key_path_available(self,bucket_name,s3_key)->bool:

        try :

            bucket = self.get_bucket(bucket_name)
            file_objects = [file_object for file_object in bucket.objects.filter(Prefix=s3_key)]

            if len(file_objects) > 0:
                return True
            return  False 
        
        except Exception as e:

            raise CustomException(e,sys)
        
    @staticmethod
    def read_object(object_name: str, decode:bool =True, make_readable:bool =False):

        try:

            logger.info("Entered into read object method")

            fun = (
                lambda: object_name.get()['Body'].read().decode()
                if decode is True
                else object_name.get()["Body"].read()
            )

            conv_fun = lambda: StringIO(fun()) if make_readable is True else fun()

            return conv_fun()

        except Exception as e:

            raise CustomException(e,sys)
        
    def get_file_object(self, filename: str, bucket_name:str):

        try:

            logger.info("Entered into get file object method")

            bucket =self.get_bucket(bucket_name)

            file_objects = [ file_object for file_object in bucket.objects.filter(Prefix=filename)]

            func = lambda x: x[0] if len(x) == 1 else x

            file_object = func(file_objects)

            return file_object

        except Exception as e:
            raise CustomException(e,sys)
    
    def create_folder(self,folder_name :str, bucket_name:str ):

        try:

            logger.info("Entered into create folder method in simple staorage class")

            self.s3_resorces.Objects(bucket_name,folder_name).load()

        except ClientError as e:

            if e.response["Error"]["Code"] == "404":

                folder_obj = folder_name + "/"
                self.s3_client.put_object(Bucket=bucket_name, key = folder_obj)
            
            else:

                pass


  
    
    def load_model(self, model_name:str,bucket_name:str ,model_dir :str = None)->object:

        try:
            logger.info("Entered in to load model function in simple storage service")
            func = (
                lambda: model_name
                if model_dir is None
                else model_dir + "/" + model_name
            )

            model_file = func()

            file_object = self.get_file_object(model_file,bucket_name)
            model_obj = self.read_object(file_object,decode = False)
            model = pickle.loads(model_obj)

            logger.info("Modle loaded from s3 bucket")

            return model

        except Exception as e:

            raise CustomException(e,sys)
        
    def upload_file(self,from_filename: str, to_filename :str,bucket_name:str,remove:bool=True):

        try :

            logger.info("Entered into upload file function (aws bucket)")

            logger.info(f"uploading  {from_filename} file to {to_filename} bucket ")

            self.s3_resorces.meta.client.upload_file(
                from_filename,bucket_name,to_filename
            )

            logger.info("File uploaded into s3 bucket")


            if remove is True:
                os.remove(from_filename)

                logger.info(f"Remove is set to {remove} .deleted the file")
            else:

                logger.info(f"Remove is set to {remove},not deleted")

        except Exception as e:

            raise CustomException(e,sys)
    


