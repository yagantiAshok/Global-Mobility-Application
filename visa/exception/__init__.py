

import sys 

class CustomException(Exception):

    def __init__(self,error_message,error_details:sys):

        self.error_message = error_message
        
        _,_,exc_tb = error_details.exc_info()

        self.line_numer = exc_tb.tb_lineno

        self.filename = exc_tb.tb_frame.f_code.co_filename

    
    def __str__(self):

        return f"Error occured in file [{self.filename} at line number [{self.line_numer} and error message is [{self.error_message}]]]"