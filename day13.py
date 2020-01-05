import numpy

class IntcodeRunner:
    registers = []
    instructionPointer = 0
    outputBuffer = []
    inputBuffer = []
    relativeBase = 0
    state = 0 # 0 is not started, 1 is done, 2 is needs input

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

    def changeDirection(self, newDir):
        if self.direction == (0, 1): # up
            if newDir == 0: # left
                self.direction = (-1, 0)
            else:
                self.direction = (1, 0)
        elif self.direction == (-1, 0): # left
            if newDir == 0:
                self.direction = (0, -1)
            else:
                self.direction = (0, 1)
        elif self.direction == (0, -1): # down
            if newDir == 0:
                self.direction = (1, 0)
            else:
                self.direction = (-1, 0)
        else: # right
            if newDir == 0:
                self.direction = (0, 1)
            else:
                self.direction = (0, -1)
    
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

def runAndGetOutput(puzzleInput):
    runner = IntcodeRunner(puzzleInput)
    runner.go()
    output = []
    while len(runner.outputBuffer) != 0:
        xPos = runner.outputBuffer.pop(0)
        yPos = runner.outputBuffer.pop(0)
        tileId = runner.outputBuffer.pop(0)
        output.append((xPos, yPos, tileId))
    return output

def part1(puzzleInput):
    output = runAndGetOutput(puzzleInput)
    blocks = 0
    for tile in output:
        if tile[2] == 2:
            blocks += 1
    print(blocks)

def drawBoard(runner):
    output = []
    while len(runner.outputBuffer) != 0:
        xPos = runner.outputBuffer.pop(0)
        yPos = runner.outputBuffer.pop(0)
        tileId = runner.outputBuffer.pop(0)
        output.append((xPos, yPos, tileId))
    map = {}
    score = -1
    for tile in output:
        if tile[0] == -1 and tile[1] == 2:
            score = tile[2]
        else:
            map[(tile[0], tile[1])] = tile[2]
    width = 44
    height = 22
    for y in range(height):
        line = ''
        for x in range(width):
            code = map[(x, y)]
            if code == 0:
                line += ' '
            else:
                line += str(code)
        print(line)

def populateMap(output):
    map = {}
    score = -1
    for tile in output:
        if tile[0] == -1 and tile[1] == 0:
            score = tile[2]
        else:
            map[(tile[0], tile[1])] = tile[2]
    return map

def getLocationOf(map, id):
    for key, value in map.items():
        if value == id:
            return key
    return (-1, -1)

def determineInput(runner):
    output = []
    while len(runner.outputBuffer) != 0:
        xPos = runner.outputBuffer.pop(0)
        yPos = runner.outputBuffer.pop(0)
        tileId = runner.outputBuffer.pop(0)
        output.append((xPos, yPos, tileId))
    map = populateMap(output)
    paddleLocation = getLocationOf(map, 3)
    ballLocation = getLocationOf(map, 4)
    if paddleLocation[0] < ballLocation[0]:
        return 1
    elif paddleLocation[0] > ballLocation[0]:
        return -1
    else:
        return 0

def getScore(runner):
    output = []
    while len(runner.outputBuffer) != 0:
        xPos = runner.outputBuffer.pop(0)
        yPos = runner.outputBuffer.pop(0)
        tileId = runner.outputBuffer.pop(0)
        output.append((xPos, yPos, tileId))
    for tile in output:
        if tile[0] == -1 and tile[1] == 0:
            return tile[2]

def part2(puzzleInput):
    runner = IntcodeRunner(puzzleInput)
    runner.registers[0] = 2
    state = runner.go()
    while state == 2:
        runner.inputBuffer.append(determineInput(runner))
        state = runner.go()
    print(getScore(runner))

f = open("day13input.txt", "r")
puzzleInput = f.read()
f.close()

part2(puzzleInput)
