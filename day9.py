import numpy

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
        for i in range(len(self.registers), 1100):
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
        print("new output:")
        print(newOutput)

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
            print("Error, invalid opcode")
    
    def go(self):
        while self.registers[self.instructionPointer] != 99:
            parameterModes, opcode, numParameters = self.interpretInstruction(self.registers[self.instructionPointer])
            if opcode == 3 and len(self.inputBuffer) == 0:
                print("needs input")
                return
            parameters = numpy.zeros(numParameters)
            for i in range(numParameters):
                parameters[i] = int(self.registers[self.instructionPointer + i + 1])
            self.executeInstruction(parameterModes, opcode, parameters)

def part1(puzzleInput):
    runner = IntcodeRunner(puzzleInput)
    runner.inputBuffer.append(1)
    runner.go()
    print("output...")
    for output in runner.outputBuffer:
        print(output)

def part2(puzzleInput):
    runner = IntcodeRunner(puzzleInput)
    runner.inputBuffer.append(2)
    runner.go()
    print("output...")
    for output in runner.outputBuffer:
        print(output)

f = open("day9input.txt", "r")
puzzleInput = f.read()
f.close()

#puzzleInput = '109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99'

part2(puzzleInput)
