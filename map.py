import cities

class Map:
    def __init__(self, filename, fucked_color):
        self.Cities = cities.setup(filename, fucked_color)

    def quarantine(self, cityName):
        cityName = cityName.lower()
        if cityName not in self.Cities:
            print cities.bcolors.FAIL + "INVALID CITY NAME " + cityName + cities.bcolors.ENDC
            return
        self.Cities[cityName].quarantine()

    def roadblock(self, cityStart, cityEnd):
        cityStart = cityStart.lower()
        cityEnd = cityEnd.lower()
        if cityStart not in self.Cities:
            print cities.bcolors.FAIL + "INVALID CITY NAME " + cityStart + cities.bcolors.ENDC
            return
        if cityEnd not in self.Cities:
            print cities.bcolors.FAIL + "INVALID CITY NAME " + cityEnd + cities.bcolors.ENDC
            return
        self.Cities[cityStart].roadblock(self.Cities[cityEnd])

    # Takes in variable number of cities. i.e. infect("TOKYO") or infect("TOKYO", "BANGKOK") etc
    def infect(self, *cities):
        for city in cities:
            city = city.lower()
            if city not in self.Cities:
                print cities.bcolors.FAIL + "INVALID CITY NAME " + city + cities.bcolors.ENDC
            self.Cities[city].infect()

    # For use in epidemics and setup, one city only
    def infectWithCount(self, city, count):
        city = city.lower()
        if city not in self.Cities:
            print cities.bcolors.FAIL + "INVALID CITY NAME " + city + cities.bcolors.ENDC
        self.Cities[city].infect(count)

    def printCity(self, city):
        city = city.lower()
        if city not in self.Cities:
            print cities.bcolors.FAIL + "INVALID CITY NAME " + city + cities.bcolors.ENDC
        print self.Cities[city]

# Covers potential actions: 
#   infect, infect with count (for epidemics and setup), quarantine, and roadblock
pandemic_map = Map("city_list.txt", "blue")
pandemic_map.quarantine("sanfrancisco")
pandemic_map.quarantine("SanFrancisco")
pandemic_map.infect("sanfrancisco")
pandemic_map.infect("sanfrancisco", "losangeles", "tokyo")
pandemic_map.infect("sanfrancisco", "sanfrancisco", "sanfrancisco")
pandemic_map.infectWithCount("losangeles", 3)
pandemic_map.roadblock("sanfrancisco","tokyo")
pandemic_map.printCity("tokyo")
pandemic_map.infect("sanfrancisco")
pandemic_map.printCity("tokyo")