


from visa.logger import logger
from visa.exception import CustomException

class TargetValuemapping:

    def __init__(self):
        self.Certified: int = 0
        self.Denied: int = 1
    
    
    def reverse_mapping(self):

        mapping_response = self.__dict__

        return dict(zip(mapping_response.values(),mapping_response.keys()))
