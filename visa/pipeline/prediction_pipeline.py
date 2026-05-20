

import sys
import pandas as pd
import numpy as np
from visa.entity.config_entity import VisaPredictionConfig
from visa.entity.s3_estimator import VisaEstimator
from visa.exception import CustomException
from visa.logger import logger
from pandas import DataFrame


class visaData:

    def __init__(self,
                continent,
                education_of_employee,
                has_job_experience,
                requires_job_training,
                no_of_employees,
                region_of_employment,
                prevailing_wage,
                unit_of_wage,
                full_time_position,
                comapny_age
                ):
        try :

                self.continent    = continent
                self.education_of_employee = education_of_employee
                self.has_job_experience = has_job_experience
                self.requires_job_training =requires_job_training
                self.no_of_employees = no_of_employees
                self.region_of_employment = region_of_employment
                self.prevailing_wagem = prevailing_wage
                self.unit_of_wage = unit_of_wage
                self.full_time_position = full_time_position
                self.comapny_age = comapny_age

        except Exception as e:
             
             raise CustomException(e,sys)
    
    def get_visa_data_as_dict(self):
         
        try:
             
            logger.info("Entered into get visa dat as dictionry method")

            input_data = {
                "continent":self.continent,
                "education_of_employee":self.education_of_employee,
                "has_job_experience":self.has_job_experience,
                "requires_job_training":self.requires_job_training,
                "no_of_employees":self.no_of_employees,
                "region_of_employment":self.region_of_employment,
                "prevailing_wage":self.prevailing_wagem,
                "unit_of_wage":self.unit_of_wage,
                "full_time_position":self.full_time_position,
                "comapny_age":  self.comapny_age
                 
            }

            return input_data
             

        except Exception as e:
             
             raise CustomException(e,sys)
        
    def get_visa_data_in_dataframe(self)->DataFrame:
         
        try:
             
            logger.info("Entered into get_visa_data_in_dataframe method ")

            data = self.get_visa_data_as_dict()

            df = pd.DataFrame([data])

            return df
              
        except Exception as e:
             
             raise CustomException(e,sys)
    

class VisaClassifier:
     
    def __init__(self,visa_prediction_config:VisaPredictionConfig= VisaPredictionConfig()):
         

        self.prediction_pipeline_config = visa_prediction_config
    
    
    def predict(self,data_frame):
         
        try:
             
            logger.info("Entered into predict method")

            model = VisaEstimator(
                bucket_name=self.prediction_pipeline_config.model_bucket_name,
                model_path=self.prediction_pipeline_config.model_file_path

            )

            result = model.predict(data_frame)

            return result

        except Exception as e:
            raise CustomException(e,sys)
             
    
        

        
              
        
        
        
                            





