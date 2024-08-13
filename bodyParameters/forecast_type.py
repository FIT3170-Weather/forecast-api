"""
A class that contains a list of all valid forecast durations

Returns:
    ForecastTypes: ForecastTypes object
"""
class ForecastType:
    def __init__(self):
        self.types = [
            "hourly",
            "daily"
            ]
        
    def getTypes(self):
        return self.types
