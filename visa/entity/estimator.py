

from sklearn.pipeline import Pipeline
from visa.logger import logger
from visa.exception import CustomException
from pandas import DataFrame
import sys

class TargetValuemapping:

    def __init__(self):
        self.Certified: int = 0
        self.Denied: int = 1
    
    
    def reverse_mapping(self):

        mapping_response = self.__dict__

        return dict(zip(mapping_response.values(),mapping_response.keys()))


class visamodel:

    def __init__(self,preprocessing_obj:Pipeline,trained_model_obj: object ):

        self.preprocessing_obj = preprocessing_obj
        self.trainded_model_obj = trained_model_obj

    def predict(self,Dataframe :DataFrame):

        try :
            logger.info("Entered into predict fundtion inside visamodel")

            transformed_features = self.preprocessing_obj.transform(Dataframe)

            logger.info("Transformed raw features into machine language")

            return self.trainded_model_obj.predict(transformed_features)

        except Exception as e:
            raise CustomException(e,sys)


        
        