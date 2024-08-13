"""
A class that contains a list of all valid locations (cities and towns).

Returns:
    Locations: Locations object
"""
class Locations:
    def __init__(self):
        self.locations = [
            "kuala-lumpur",
            "petaling-jaya",
            "subang-jaya",
            "ipoh"
            ]
        
    def getLocations(self):
        return self.locations
