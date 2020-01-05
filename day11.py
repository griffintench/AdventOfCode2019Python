import numpy

class Robot:
    registers = []
    instructionPointer = 0
    outputBuffer = []
    inputBuffer = []
    relativeBase = 0
    location = (0, 0)
    direction = (0, 1)
    panels = {} # true = white, false = black

    def __init__(self, puzzleInput):
        self.registers = puzzleInput.split(',')
        for i, item in enumerate(self.registers):
            self.registers[i] = int(item)
        for i in range(len(self.registers), 1200):
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
            if len(self.inputBuffer) == 0:
                self.inputBuffer.append(1 if self.location in self.panels.keys() and self.panels[self.location] else 0)
            parameterModes, opcode, numParameters = self.interpretInstruction(self.registers[self.instructionPointer])
            #print(str(self.instructionPointer))
            #print('opcode: ' + str(opcode))
            parameters = numpy.zeros(numParameters)
            for i in range(numParameters):
                parameters[i] = int(self.registers[self.instructionPointer + i + 1])
            self.executeInstruction(parameterModes, opcode, parameters)
            if len(self.outputBuffer) == 2:
                #print('current location: ' + str(self.location))
                #print('current direction: ' + str(self.direction))
                #print('output: ' + str(self.outputBuffer[0]) + ', ' + str(self.outputBuffer[1]))
                colour = self.outputBuffer.pop(0)
                self.panels[self.location] = colour == 1
                #print('new colour: ' + str(self.panels[self.location]))
                dir = self.outputBuffer.pop(0)
                self.changeDirection(dir)
                self.location = (self.location[0] + self.direction[0], self.location[1] + self.direction[1])
                self.inputBuffer = []
                newColour = 1 if self.location in self.panels.keys() and self.panels[self.location] else 0
                self.inputBuffer.append(newColour)
                #print('new location: ' + str(self.location))
                #print('new direction: ' + str(self.direction))
        print(len(self.panels.keys()))

def part1(puzzleInput):
    robot = Robot(puzzleInput)
    robot.panels[(0, 0)] = False
    robot.go()

def part2(puzzleInput):
    robot = Robot(puzzleInput)
    robot.panels[(0, 0)] = True
    robot.go()
    minX = 10000000
    maxX = -10000000
    minY = 10000000
    maxY = -10000000
    for location in robot.panels.keys():
        if location[0] < minX:
            minX = location[0]
        if location[0] > maxX:
            maxX = location[0]
        if location[1] < minY:
            minY = location[1]
        if location[1] > maxY:
            maxY = location[1]
    for y in reversed(range(minY, maxY + 1)):
        currentLine = ''
        for x in range(minX, maxX + 1):
            if (x, y) in robot.panels.keys() and robot.panels[(x, y)]:
                currentLine += '#'
            else:
                currentLine += '.'
        print(currentLine)

f = open("day11input.txt", "r")
puzzleInput = f.read()
f.close()

#puzzleInput = '1101,0,99,501,3,500,1005,500,501,104,1,104,0,104,0,104,0,104,1,104,0,104,1,104,0,3,500,1005,500,501,104,26,99'

part2(puzzleInput)
