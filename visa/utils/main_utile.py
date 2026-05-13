import sys
import yaml
from visa.exception import CustomException
from visa.logger import logger
from box import ConfigBox
from pathlib import Path
from ensure import ensure_annotations
import dill
import os
from pandas import DataFrame

@ensure_annotations
def read_yaml(file_path:Path)->ConfigBox:
    try:
        with open(file_path) as file:

            data = yaml.safe_load(file)
        
        data = ConfigBox(data)

        return data

    except Exception as e:
        raise CustomException(e,sys)
    
@ensure_annotations
def write_to_yaml(file_path:str,data):

    try:
        logger.info("duming data ingo yaml file")

        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path,exist_ok=True)

        with open(file_path,"w") as file:

            yaml.dump(data,file)

    except Exception as e:
         raise CustomException(e,sys)


@ensure_annotations
def load_object(file_path:str)->object:
    logger.info("Entered The load object method")

    try:

        with open(file_path,"rb") as file_obj:

            obj = dill.load(file_obj)
        
        logger.info("Object loaded")

        return obj
    except Exception as e:

        raise CustomException(e,sys)

@ensure_annotations

def save_object(file_path:str ,data):
    logger.info("Entered the save object method")

    try:
        os.makedirs(os.path.dirname(file_path),exist_ok=True)
        with open(file_path,"wb") as file:

            dill.dump(data,file)
        logger.info("Model saved as object")

    except Exception as e:
        raise CustomException(e,sys)
    
@ensure_annotations

def drop_columns(df:DataFrame,cols:list)->DataFrame:

    try:

        logger.info("Entered the drop column method")

        df = df.drop(columns=cols)

        logger.infor("unwanted columns dropped")

        return df
    
    except Exception as e:
        raise CustomException(e,sys)