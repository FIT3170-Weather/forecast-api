"""
A class that contains a list of all valid weather variables

Returns:
    Variables: Variables object
"""
class Variables:
    def __init__(self):
        self.variables = [
            "temperature",
            "precipitation",
            "humidity",
            "wind",
            "pressure",
            "visibility",
            "cloud",
            "condition"
            ]
        
    def getVariables(self):
        return self.variables
