import sys
from src.logger import logging

def error_message_details(error, error_details:sys):
    _,_,exc_tb = error_details.exc.info()
    file_name = exc_tb.tb_frame.f_code.co_filename
    file_loc = exc_tb.tb_lineno
    error_message = f'Error occured in python script name{file_name}, line no{file_loc} and error message {str(error)}'
    
    
    return error_message


class CustomException(Exception):
    def __init__(self, error_message, error_details:sys):
        super().__init__(error_message)
        self.error_message=error_message_details(error=error_message, error_details=error_details)


    def __str__(self):
        return self.error_message