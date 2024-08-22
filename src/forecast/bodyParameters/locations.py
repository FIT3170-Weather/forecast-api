"""
A class that contains a list of all valid locations (cities and towns).

Returns:
    Locations: Locations object
"""
class Locations:
    def __init__(self):
        self.locations = {
            "kuala-lumpur": {"lat": 3.1319, "lon": 101.6841},
            "petaling-jaya": {"lat": 3.1279, "lon": 101.5945},
            "subang-jaya": {"lat": 3.057, "lon": 101.585},
            "ipoh": {"lat": 4.6005, "lon": 101.0758},
            "johor-bahru": {"lat": 1.4655, "lon": 103.7578}
        }
        
    def getLocations(self):
        return self.locations
