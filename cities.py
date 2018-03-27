import sys

# some stuff to help with printing in pretty colours
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class City:
    COLORS = ["RED", "YELLOW", "BLACK", "BLUE", "FUCKED"]
    MAX_INFECTION = 3

    # Initialisation. Requires name, color and list of connections
    def __init__(self, name, color, connections):
        # public variables
        self.name = name
        if color.upper() not in City.COLORS:
            print bcolors.FAIL + "Invalid Colour Given" + bcolors.ENDC
        self.color = color.upper()
        # private variables (cannot be accessed outside this class)
        self.__connections = connections 
        self.__roadBlocks = [False for i in connections]
        self.__infectionCount = [0 for c in City.COLORS];
        self.__isQuarantined = False

    # Print contents of city neatly
    def __str__(self):
        string = bcolors.UNDERLINE + bcolors.BOLD + self.name.upper() + bcolors.ENDC + "\n"
        string += "QUARANTINED: " + str(self.__isQuarantined) + "\n"
        string += "INFECTION STATUS:"
        for (i,colour) in enumerate(City.COLORS):
            if self.__infectionCount[i] > 0:
                if self.__infectionCount[i] == City.MAX_INFECTION - 1:
                    string += bcolors.WARNING
                elif self.__infectionCount[i] == City.MAX_INFECTION:
                    string += bcolors.FAIL
                else:
                    string += bcolors.OKBLUE
                string += " " + colour + ": " + str(self.__infectionCount[i])
                string += bcolors.ENDC
        string += "\nCONNECTIONS:"
        for (i,city) in enumerate(self.__connections):
            if self.__roadBlocks[i]:
                string += bcolors.OKBLUE
            string += " " + city.name
            if self.__roadBlocks[i]:
                string += bcolors.ENDC
        return string

    # Equality check
    def __eq__(self, other):
        return self.name == other.name

    # Add a connected city
    def addConnection(self, city):
        if city in self.__connections:
            print bcolors.WARNING + "City already connected." + bcolors.ENDC
            return
        self.__connections.append(city)
        self.__roadBlocks.append(False)

    def quarantine(self):
        if self.__isQuarantined:
            print bcolors.WARNING + "Already Quarantined" + bcolors.ENDC
        self.__isQuarantined = True

    def roadblock(self, city):
        if city not in self.__connections:
            print bcolors.FAIL + "Trying to roadblock unconnected city" + bcolors.ENDC
        index = self.__connections.index(city)
        if self.__roadBlocks[index]:
            return
        self.__roadBlocks[index] = True
        city.roadblock(self)
        
    def infectWithCountAndColor(self, number, color):
        if color.upper() not in City.COLORS:
            print bcolors.FAIL + "Invalid Colour Given" + bcolors.ENDC
            return
        if self.__isQuarantined:
            print bcolors.OKGREEN + "City not infected: Was quarantined." + bcolors.ENDC
            self.__isQuarantined = False
            return
        index = City.COLORS.index(color.upper())
        self.__infectionCount[index] += number
        if (self.__infectionCount[index] > City.MAX_INFECTION):
            difference = self.__infectionCount[index] - City.MAX_INFECTION
            self.__infectionCount[index] = City.MAX_INFECTION
            print bcolors.FAIL + "OUTBREAK IN " + self.name + ". INCREASE PANIC LEVEL" + bcolors.ENDC
            for i in range(len(self.__connections)):
                if self.__roadBlocks[i]:
                    string = bcolors.OKGREEN + "Outbreak prevented in "
                    string += self.__connections[i].name + ": Roadblock present." + bcolors.ENDC
                    continue
                self.__connections[i].infectWithCountAndColor(difference, color)
            return
        

    # If no colour given, infect with own colour
    def infectWithCount(self, number):
        self.infectWithCountAndColor(number, self.color)

    # If no arguments given, infect self with own colour and 1 cube
    def infect(self):
        self.infectWithCount(1)

def setup(filename):
    print "Importing cities from " + sys.argv[1]
    with open(filename, "r") as file:
        for line in file:
            words = line.split()
            if (len(words) > 2):
                name = words[0]
                colour = words[1]
                city = City(name, colour, [])
                if name in Cities:
                    city = Cities[name]
                else:
                    Cities[name] = city 
                city.color = colour.upper()
                for connection_name in words[2:]:
                    connection = City(connection_name, "FUCKED", [])
                    if connection_name in Cities:
                        connection = Cities[connection_name]
                    else:
                        Cities[connection_name] = connection
                    connection.addConnection(city)
                    city.addConnection(connection)


Cities = {}

if len(sys.argv) > 1:
    setup(sys.argv[1])
    
print "List of Cities"
print sorted(Cities.keys())

# basic tests
def testFunctions():
    global Cities
    SF = Cities["SanFrancisco"]
    LA = Cities["LosAngeles"]

    print "\nInitial city states"
    print SF
    print LA
    # Infect SF, make sure LA gets a blue cube
    print "\nInfecting SF"
    SF.infect()
    print SF
    print "\nQuarantining SF"
    SF.quarantine()
    print SF
    print "\nQuarantining again (shouldn't do anything)"
    SF.quarantine()
    print SF
    print "\nInfecting SF. Should remove quarantine."
    SF.infect()
    print SF
    print "\nInfect SF three times. Should cause outbreak into LA."
    SF.infect()
    SF.infect()
    SF.infect()
    print SF
    print LA
    # Roadblock and infect again (expect LA to be unaffected)
    print "\nRoadblock SF<->LA. Note: If a connection is printed in blue, it's roadblocked."
    SF.roadblock(LA)
    print SF
    print LA
    print "\nInfect SF. Should not affect LA."
    SF.infect()
    print SF 
    print LA
    # Infect LA three times (with yellow)
    print "\nInfect LA three times. Should see yellow increase."
    LA.infectWithCount(3)
    print LA
    print "\nPrinting rest of cities connected to SF"
    print Cities["Tokyo"]
    print Cities["Manila"]
    print Cities["Chicago"]

# Uncomment to run tests
# testFunctions()


