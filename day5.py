import numpy

def getParameters(opcode):
    numParameters = [0, 3, 3, 1, 1, 2, 2, 3, 3]
    return numParameters[opcode]

def interpretInstruction(instruction):
    strInstruction = str(instruction)
    opcode = int(strInstruction[-2:])
    modeString = strInstruction[:-2]
    parameters = getParameters(opcode)
    parameterModes = numpy.zeros(parameters)
    i = 0
    for c in reversed(modeString):
        if c == '1':
            parameterModes[i] = 1
        i += 1
    return parameterModes, opcode, parameters

def getOperand(parameterMode, parameter, registers):
    if parameterMode == 0:
        return int(registers[int(parameter)])
    return int(parameter)

def add(parameterModes, parameters, registers, instructionPointer):
    operand1 = getOperand(parameterModes[0], parameters[0], registers)
    operand2 = getOperand(parameterModes[1], parameters[1], registers)
    registers[int(parameters[2])] = operand1 + operand2
    return instructionPointer + 4

def multiply(parameterModes, parameters, registers, instructionPointer):
    operand1 = getOperand(parameterModes[0], parameters[0], registers)
    operand2 = getOperand(parameterModes[1], parameters[1], registers)
    registers[int(parameters[2])] = operand1 * operand2
    return instructionPointer + 4

def saveInput(parameters, input, registers, instructionPointer):
    registers[int(parameters[0])] = input
    return instructionPointer + 2

def printOutput(parameterModes, parameters, registers, instructionPointer):
    print('output')
    print(getOperand(parameterModes[0], parameters[0], registers))
    return instructionPointer + 2

def jumpIfTrue(parameterModes, parameters, registers, instructionPointer):
    operand1 = getOperand(parameterModes[0], parameters[0], registers)
    operand2 = getOperand(parameterModes[1], parameters[1], registers)
    if operand1 != 0:
        return operand2
    else:
        return instructionPointer + 3

def jumpIfFalse(parameterModes, parameters, registers, instructionPointer):
    operand1 = getOperand(parameterModes[0], parameters[0], registers)
    operand2 = getOperand(parameterModes[1], parameters[1], registers)
    if operand1 == 0:
        return operand2
    else:
        return instructionPointer + 3

def lessThan(parameterModes, parameters, registers, instructionPointer):
    operand1 = getOperand(parameterModes[0], parameters[0], registers)
    operand2 = getOperand(parameterModes[1], parameters[1], registers)
    registers[int(parameters[2])] = 1 if operand1 < operand2 else 0
    return instructionPointer + 4

def equals(parameterModes, parameters, registers, instructionPointer):
    operand1 = getOperand(parameterModes[0], parameters[0], registers)
    operand2 = getOperand(parameterModes[1], parameters[1], registers)
    registers[int(parameters[2])] = 1 if operand1 == operand2 else 0
    return instructionPointer + 4

def executeInstruction(parameterModes, opcode, parameters, input, registers, instructionPointer):
    if opcode == 1:
        return add(parameterModes, parameters, registers, instructionPointer)
    elif opcode == 2:
        return multiply(parameterModes, parameters, registers, instructionPointer)
    elif opcode == 3:
        return saveInput(parameters, input, registers, instructionPointer)
    elif opcode == 4:
        return printOutput(parameterModes, parameters, registers, instructionPointer)
    elif opcode == 5:
        return jumpIfTrue(parameterModes, parameters, registers, instructionPointer)
    elif opcode == 6:
        return jumpIfFalse(parameterModes, parameters, registers, instructionPointer)
    elif opcode == 7:
        return lessThan(parameterModes, parameters, registers, instructionPointer)
    elif opcode == 8:
        return equals(parameterModes, parameters, registers, instructionPointer)
    else:
        print("Error, invalid opcode")

def part1(puzzleInput):
    registers = puzzleInput.split(',')
    for i, item in enumerate(registers):
        registers[i] = int(item)
    input = 1
    instructionPointer = 0
    while registers[instructionPointer] != 99:
        print(instructionPointer)
        if False and instructionPointer == 46:
            print("error with this instruction?")
            print(registers[46:50])
        parameterModes, opcode, numParameters = interpretInstruction(registers[instructionPointer])
        parameters = numpy.zeros(numParameters)
        for i in range(numParameters):
            parameters[i] = int(registers[instructionPointer + i + 1])
        executeInstruction(parameterModes, opcode, parameters, input, registers)
        instructionPointer += numParameters + 1

def part2(puzzleInput):
    registers = puzzleInput.split(',')
    for i, item in enumerate(registers):
        registers[i] = int(item)
    input = 5
    instructionPointer = 0
    while registers[instructionPointer] != 99:
        print(instructionPointer)
        if False and instructionPointer == 46:
            print("error with this instruction?")
            print(registers[46:50])
        parameterModes, opcode, numParameters = interpretInstruction(registers[instructionPointer])
        parameters = numpy.zeros(numParameters)
        for i in range(numParameters):
            parameters[i] = int(registers[instructionPointer + i + 1])
        instructionPointer = executeInstruction(parameterModes, opcode, parameters, input, registers, instructionPointer)

f = open("day5input.txt", "r")
puzzleInput = f.read()
f.close()
#puzzleInput = '3,0,104,0,99'

part2(puzzleInput)
