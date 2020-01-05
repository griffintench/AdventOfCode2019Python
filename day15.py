import numpy

NORTH = 1
SOUTH = 2
WEST = 3
EAST = 4

class IntcodeRunner:
    registers = []
    instructionPointer = 0
    outputBuffer = []
    inputBuffer = []
    relativeBase = 0

    def __init__(self, puzzleInput):
        self.registers = puzzleInput.split(',')
        for i, item in enumerate(self.registers):
            self.registers[i] = int(item)
        for i in range(len(self.registers), 2600):
            self.registers.append(0)

    def addInput(self, newInput):
        self.inputBuffer.append(newInput)

    def getOutput(self):
        return self.outputBuffer.pop(0)

    def getParameters(self, opcode):
        numParameters = [0, 3, 3, 1, 1, 2, 2, 3, 3, 1]
        return numParameters[opcode]

    def interpretInstruction(self, instruction):
        strInstruction = str(instruction)
        opcode = int(strInstruction[-2:])
        modeString = strInstruction[:-2]
        parameters = self.getParameters(opcode)
        parameterModes = numpy.zeros(parameters)
        i = 0
        for c in reversed(modeString):
            if c == '1':
                parameterModes[i] = 1
            elif c == '2':
                parameterModes[i] = 2
            i += 1
        return parameterModes, opcode, parameters

    def getOperand(self, parameterMode, parameter):
        if parameterMode == 0:
            return int(self.registers[int(parameter)])
        elif parameterMode == 2:
            return int(self.registers[int(parameter) + self.relativeBase])
        return int(parameter)

    def getAddress(self, parameterMode, parameter):
        if parameterMode == 2:
            return int(parameter) + self.relativeBase
        else:
            return int(parameter)

    def add(self, parameterModes, parameters):
        operand1 = self.getOperand(parameterModes[0], parameters[0])
        operand2 = self.getOperand(parameterModes[1], parameters[1])
        returnAddress = self.getAddress(parameterModes[2], parameters[2])
        self.registers[returnAddress] = operand1 + operand2
        self.instructionPointer += 4

    def multiply(self, parameterModes, parameters):
        operand1 = self.getOperand(parameterModes[0], parameters[0])
        operand2 = self.getOperand(parameterModes[1], parameters[1])
        returnAddress = self.getAddress(parameterModes[2], parameters[2])
        self.registers[returnAddress] = operand1 * operand2
        self.instructionPointer += 4

    def saveInput(self, parameterModes, parameters):
        address = self.getAddress(parameterModes[0], parameters[0])
        self.registers[address] = self.inputBuffer.pop(0)
        self.instructionPointer += 2

    def getOutput(self, parameterModes, parameters):
        newOutput = self.getOperand(parameterModes[0], parameters[0])
        self.outputBuffer.append(newOutput)
        self.instructionPointer += 2

    def jumpIfTrue(self, parameterModes, parameters):
        operand1 = self.getOperand(parameterModes[0], parameters[0])
        operand2 = self.getOperand(parameterModes[1], parameters[1])
        if operand1 != 0:
            self.instructionPointer = operand2
        else:
            self.instructionPointer += 3

    def jumpIfFalse(self, parameterModes, parameters):
        operand1 = self.getOperand(parameterModes[0], parameters[0])
        operand2 = self.getOperand(parameterModes[1], parameters[1])
        if operand1 == 0:
            self.instructionPointer = operand2
        else:
            self.instructionPointer += 3

    def lessThan(self, parameterModes, parameters):
        operand1 = self.getOperand(parameterModes[0], parameters[0])
        operand2 = self.getOperand(parameterModes[1], parameters[1])
        returnAddress = self.getAddress(parameterModes[2], parameters[2])
        self.registers[returnAddress] = 1 if operand1 < operand2 else 0
        self.instructionPointer += 4

    def equals(self, parameterModes, parameters):
        operand1 = self.getOperand(parameterModes[0], parameters[0])
        operand2 = self.getOperand(parameterModes[1], parameters[1])
        returnAddress = self.getAddress(parameterModes[2], parameters[2])
        self.registers[returnAddress] = 1 if operand1 == operand2 else 0
        self.instructionPointer += 4

    def changeRelativeBase(self, parameterModes, parameters):
        operand = self.getOperand(parameterModes[0], parameters[0])
        self.relativeBase += operand
        self.instructionPointer += 2

    def executeInstruction(self, parameterModes, opcode, parameters):
        if opcode == 1:
            self.add(parameterModes, parameters)
        elif opcode == 2:
            self.multiply(parameterModes, parameters)
        elif opcode == 3:
            self.saveInput(parameterModes, parameters)
        elif opcode == 4:
            self.getOutput(parameterModes, parameters)
        elif opcode == 5:
            self.jumpIfTrue(parameterModes, parameters)
        elif opcode == 6:
            self.jumpIfFalse(parameterModes, parameters)
        elif opcode == 7:
            self.lessThan(parameterModes, parameters)
        elif opcode == 8:
            self.equals(parameterModes, parameters)
        elif opcode == 9:
            self.changeRelativeBase(parameterModes, parameters)
        else:
            print("Error, invalid opcode: " + str(opcode))
    
    def go(self):
        while self.registers[self.instructionPointer] != 99:
            parameterModes, opcode, numParameters = self.interpretInstruction(self.registers[self.instructionPointer])
            if opcode == 3 and len(self.inputBuffer) == 0:
                return 2
            parameters = numpy.zeros(numParameters)
            for i in range(numParameters):
                parameters[i] = int(self.registers[self.instructionPointer + i + 1])
            self.executeInstruction(parameterModes, opcode, parameters)
        return 1

class MapTraverser:
    location = (0, 0)
    map = {}
    def __init__(self, puzzleInput):
        self.runner = IntcodeRunner(puzzleInput)
        self.map[self.location] = 1

    # returns (pathLength, nextDir)
    def shortestPath(self, fromLocation, toLocation):
        if fromLocation == toLocation:
            return 0
        shortestPathsMap = {}
        shortestPathsMap[fromLocation] = (0, 0)
        northLocation = (fromLocation[0], fromLocation[1] + 1)
        if northLocation in self.map.keys() and self.map[northLocation] != 0:
            shortestPathsMap[northLocation] = (1, NORTH)
        southLocation = (fromLocation[0], fromLocation[1] - 1)
        if southLocation in self.map.keys() and self.map[southLocation] != 0:
            shortestPathsMap[southLocation] = (1, SOUTH)
        westLocation = (fromLocation[0] - 1, fromLocation[1])
        if westLocation in self.map.keys() and self.map[westLocation] != 0:
            shortestPathsMap[westLocation] = (1, WEST)
        eastLocation = (fromLocation[0] + 1, fromLocation[1])
        if eastLocation in self.map.keys() and self.map[eastLocation] != 0:
            shortestPathsMap[eastLocation] = (1, EAST)
        i = 1
        while toLocation not in shortestPathsMap.keys():
            temp = {}
            for key, value in shortestPathsMap.items():
                if value[0] == i:
                    northLocation = (key[0], key[1] + 1)
                    if northLocation not in shortestPathsMap.keys() and northLocation in self.map.keys() and self.map[northLocation] != 0:
                        temp[northLocation] = (i + 1, value[1])
                    southLocation = (key[0], key[1] - 1)
                    if southLocation not in shortestPathsMap.keys() and southLocation in self.map.keys() and self.map[southLocation] != 0:
                        temp[southLocation] = (i + 1, value[1])
                    westLocation = (key[0] - 1, key[1])
                    if westLocation not in shortestPathsMap.keys() and westLocation in self.map.keys() and self.map[westLocation] != 0:
                        temp[westLocation] = (i + 1, value[1])
                    eastLocation = (key[0] + 1, key[1])
                    if eastLocation not in shortestPathsMap.keys() and eastLocation in self.map.keys() and self.map[eastLocation] != 0:
                        temp[eastLocation] = (i + 1, value[1])
            for key, value in temp.items():
                shortestPathsMap[key] = value
            i += 1
        return shortestPathsMap[toLocation]

    def findSpaceWithAdjacentMove(self):
        for key, value in self.map.items():
            if value != 0:
                northLocation = (key[0], key[1] + 1)
                southLocation = (key[0], key[1] - 1)
                westLocation = (key[0] - 1, key[1])
                eastLocation = (key[0] + 1, key[1])
                if northLocation not in self.map.keys() or southLocation not in self.map.keys() or westLocation not in self.map.keys() or eastLocation not in self.map.keys():
                    return key
        return None

    def determineNextMove(self):
        northLocation = (self.location[0], self.location[1] + 1)
        if northLocation not in self.map.keys():
            return NORTH
        southLocation = (self.location[0], self.location[1] - 1)
        if southLocation not in self.map.keys():
            return SOUTH
        westLocation = (self.location[0] - 1, self.location[1])
        if westLocation not in self.map.keys():
            return WEST
        eastLocation = (self.location[0] + 1, self.location[1])
        if eastLocation not in self.map.keys():
            return EAST
        toLocation = self.findSpaceWithAdjacentMove()
        pathLength, nextDir = self.shortestPath(self.location, toLocation)
        return nextDir

    def makeMove(self):
        dir = self.determineNextMove()
        nextLocation = self.location
        if dir == NORTH:
            nextLocation = (self.location[0], self.location[1] + 1)
        elif dir == SOUTH:
            nextLocation = (self.location[0], self.location[1] - 1)
        elif dir == WEST:
            nextLocation = (self.location[0] - 1, self.location[1])
        elif dir == EAST:
            nextLocation = (self.location[0] + 1, self.location[1])
        while len(self.runner.outputBuffer) == 0:
            self.runner.inputBuffer = []
            self.runner.inputBuffer.append(dir)
            self.runner.go()
        output = self.runner.outputBuffer.pop(0)
        if output == 0:
            self.map[nextLocation] = output
        elif output == 1 or output == 2:
            self.map[nextLocation] = output
            self.location = nextLocation
        #print(self.location)
        #print(output)
        return output

    def isMapComplete(self):
        for key, value in self.map.items():
            if value != 0:
                northLocation = (key[0], key[1] + 1)
                southLocation = (key[0], key[1] - 1)
                westLocation = (key[0] - 1, key[1])
                eastLocation = (key[0] + 1, key[1])
                if northLocation not in self.map.keys():
                    return False
                if southLocation not in self.map.keys():
                    return False
                if westLocation not in self.map.keys():
                    return False
                if eastLocation not in self.map.keys():
                    return False
        return True

    def getOxygenLocation(self):
        for key, value in self.map.items():
            if value == 2:
                return key
        return None

    def fillWithOxygen(self):
        start = self.getOxygenLocation()
        time = 0
        filled = [start]
        done = False
        while not done:
            done = True
            temp = []
            for key, value in self.map.items():
                if value != 0 and key not in filled:
                    northLocation = (key[0], key[1] + 1)
                    southLocation = (key[0], key[1] - 1)
                    westLocation = (key[0] - 1, key[1])
                    eastLocation = (key[0] + 1, key[1])
                    if northLocation in filled or southLocation in filled or westLocation in filled or eastLocation in filled:
                        done = False
                        temp.append(key)
            for location in temp:
                filled.append(location)
            if not done:
                time += 1
        return time

def part1(puzzleInput):
    mapTraverser = MapTraverser(puzzleInput)
    output = 1
    while output != 2:
        output = mapTraverser.makeMove()
    print(mapTraverser.location)
    pathLength, nextDir = mapTraverser.shortestPath((0, 0), mapTraverser.location)
    print(pathLength)

def part2(puzzleInput):
    mapTraverser = MapTraverser(puzzleInput)
    #mapTraverser.map = { (0, 0): 0, (-1, 0): 1, (-2, 0): 0, (1, 0): 1, (2, 0): 1, (3, 0): 0, (-2, 1): 0, (-1, 1): 1, (0, 1): 1, (1, 1): 0, (2, 1): 0, (-1, 2): 0, (0, 2): 0, (-2, -1): 0, (-1, -1): 1, (0, -1): 2, (1, -1): 1, (2, -1): 0, (-1, -2): 0, (0, -2): 0, (1, -2): 0 }
    while not mapTraverser.isMapComplete():
        mapTraverser.makeMove()
    print(mapTraverser.fillWithOxygen())

f = open("day15input.txt", "r")
puzzleInput = f.read()
f.close()

part2(puzzleInput)
