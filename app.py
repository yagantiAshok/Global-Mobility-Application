

class TargetValuemapping:

    value = None

    def __init__(self):
        self.Certified:int = 0
        self.Denied:int = 1

# obj  = TargetValuemapping()

# print(obj.__dict__)

print(TargetValuemapping().__dict__)