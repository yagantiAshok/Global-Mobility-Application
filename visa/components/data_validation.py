
import sys
from visa.entity.config_entity import DataValidationConfig
from visa.entity.artifact_entity import DataIngestionArtifact
from visa.logger import logger
from visa.exception import CustomException
from visa.constants import SCHEMA_FILE
import pandas as pd
from visa.utils.main_utile import create_directories,read_yaml


class Datavalidation:

    def __init__(self,data_validation:DataValidationConfig):
        
        try :

            self.data_validation_config = data_validation
            self.schema_file = read_yaml(SCHEMA_FILE)

        except Exception as e:
            raise CustomException(e,sys)
    
    def validating_testset_columns(self,test_data_path):
            
        logger.info("Entered into validating_test_set_columns module")

        try :

            test_data = pd.read_csv(test_data_path)

            Validation_status = True

            error_messages = []

            # Getting Schema Deatils

            schema_all_data  = self.schema_file.all_columns

            expected_columns = list(self.schema_file.all_columns.keys())

            expected_numerical_columns = list(self.schema_file.numerical_columns)

            cexpected_categorical_columns   = list(self.schema_file.categorical_columns)

            # getting test dat columns

            actual_columns = list(test_data.columns)

            """
            1. CHECKING MISSING COLUMNS

            """
            missing_columns = []

            for column in expected_columns:

                if column not in actual_columns:

                    missing_columns.append(column)

            if (len(missing_columns))>0:

                Validation_status = False

                error_messages.append(
                    f"Missing_columns: {missing_columns}"
                )
            
            logger.info(f"MISSING COLUMNS ARE {missing_columns}")

            """
            2.CHECKING EXTRA COLUMNS 
            
            """

            extra_columns = []

            for column in actual_columns:

                if column not in expected_columns:

                    extra_columns.append(column)

            if (len(extra_columns))>0:

                Validation_status = False

                error_messages.append(
                    f"Extra Columns Are : {extra_columns}"
                )

            logger.info(f"EXTRA COLUMNS ARE : {extra_columns}")

            """
            3.CHECKING SCHEMA OF DATA

            """

            schema_validation = []

            for column,expected_type in schema_all_data.items():

                if column in actual_columns:

                    actual_data_type  = str(test_data[column].dtype)

                    if expected_type!=actual_data_type:

                        schema_validation.append({
                            "Column":column,
                            "expected_type":expected_type,
                            "Actual_type" : actual_data_type
                        })
                if (len(schema_validation))>0:

                    Validation_status = False

                    error_messages.append(
                        f"Schema Validation : {schema_validation}"
                    )
            
            logger.info(f"DATA TYPE NOT MATCHED columns are : {schema_validation}")
            
            """
            4.CHECKING NUMARICAL COLUMNS 

            """
            numerical_columns = []

            for column in expected_numerical_columns:

                if column not in actual_columns:

                    numerical_columns.append(column)

            if (len(numerical_columns))>0:
                    
                    Validation_status = False

                    error_messages.append(
                        f"Extra Columns Are : {numerical_columns}"
                    )

            logger.info(f"MISSED NUMARICAL  COLUMNS ARE : {numerical_columns}")

            """
            5.CHECKING CATEGORICAL COLUMNS
            
            """
            categorical_columns = []

            for column in cexpected_categorical_columns:

                if column not in actual_columns:

                    categorical_columns.append(column)


            if (len(categorical_columns))>0:
                    
                    Validation_status = False

                    error_messages.append(
                        f"Extra Columns Are : {categorical_columns}"
                    )

            logger.info(f"MISSED CATEGORICAL  COLUMNS ARE : {categorical_columns}")

            """
            6.DUPLICATE ROWS VALIDATION
            
            """

            duplicated_rows = test_data.duplicated().sum()

            if duplicated_rows >0:

                error_messages.append(f"DUPLICATED ROWS FOUND  {duplicated_rows}")
            
            logger.info(f"DUPLICATED ROWS  {duplicated_rows}")

            """
            7.MISSING VALUE COLUMNS PERCENTAGE 
            
            """

            nan_value_columns = []

            for column in actual_columns:

                missingness = test_data[column].isnull().mean()*100

                if missingness>0:

                    nan_value_columns.append({
                        "Column":column,
                        "Nan Percentage": round(missingness)  
                    })


            logger.info(f"NAN COLUMNS {nan_value_columns}")

            """
            8. FINAL VALIDATION REPORT 

            """

            create_directories(self.data_validation_config.data_validation_status_path)

            with open(self.data_validation_config.data_validation_status_path,"w") as file:

                file.write(f"DATA VALIDATION STATUS : {Validation_status} \n\n")

                for messages in error_messages:

                    file.write(messages + "\n")
            
            logger.info(f"FINAL VALIDATION STATUS {Validation_status}")

            return Validation_status


            
        except Exception as e:
    
            raise CustomException(e,sys)
    

        

            
        