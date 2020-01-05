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

def getOutput(parameterModes, parameters, registers, instructionPointer):
    output = getOperand(parameterModes[0], parameters[0], registers)
    return instructionPointer + 2, output

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
        return add(parameterModes, parameters, registers, instructionPointer), -1, False
    elif opcode == 2:
        return multiply(parameterModes, parameters, registers, instructionPointer), -1, False
    elif opcode == 3:
        return saveInput(parameters, input, registers, instructionPointer), -1, True
    elif opcode == 4:
        newInstructionPointer, output = getOutput(parameterModes, parameters, registers, instructionPointer)
        return newInstructionPointer, output, False
    elif opcode == 5:
        return jumpIfTrue(parameterModes, parameters, registers, instructionPointer), -1, False
    elif opcode == 6:
        return jumpIfFalse(parameterModes, parameters, registers, instructionPointer), -1, False
    elif opcode == 7:
        return lessThan(parameterModes, parameters, registers, instructionPointer), -1, False
    elif opcode == 8:
        return equals(parameterModes, parameters, registers, instructionPointer), -1, False
    else:
        print("Error, invalid opcode")

def runProgram(registers, input1, input2):
    for i, item in enumerate(registers):
        registers[i] = int(item)
    instructionPointer = 0
    input = input1
    output = -1
    while registers[instructionPointer] != 99:
        parameterModes, opcode, numParameters = interpretInstruction(registers[instructionPointer])
        parameters = numpy.zeros(numParameters)
        for i in range(numParameters):
            parameters[i] = int(registers[instructionPointer + i + 1])
        instructionPointer, newOutput, switchInput = executeInstruction(parameterModes, opcode, parameters, input, registers, instructionPointer)
        if switchInput:
            input = input2
        if newOutput != -1:
            output = newOutput
    return output

def runAllPrograms(puzzleInput, phaseSettings):
    aOutput = runProgram(puzzleInput.split(','), phaseSettings[0], 0)
    bOutput = runProgram(puzzleInput.split(','), phaseSettings[1], aOutput)
    cOutput = runProgram(puzzleInput.split(','), phaseSettings[2], bOutput)
    dOutput = runProgram(puzzleInput.split(','), phaseSettings[3], cOutput)
    eOutput = runProgram(puzzleInput.split(','), phaseSettings[4], dOutput)
    return eOutput

def getAllPermutations(masterList, aList, i, length):
    if i == length:
        masterList.append(aList.copy())
    else:
        for j in range(i, length):
            aList[i], aList[j] = aList[j], aList[i]
            getAllPermutations(masterList, aList, i + 1, length)
            aList[i], aList[j] = aList[j], aList[i]

def getAllPhaseSettings(basicPhaseSettings):
    phaseSettingsList = []
    getAllPermutations(phaseSettingsList, basicPhaseSettings, 0, 5)
    return phaseSettingsList

def part1(puzzleInput):
    basicPhaseSettings = [0, 1, 2, 3, 4]
    phaseSettingsList = getAllPhaseSettings(basicPhaseSettings)
    maxOutput = -1
    for phaseSettings in phaseSettingsList:
        output = runAllPrograms(puzzleInput, phaseSettings)
        if output > maxOutput:
            maxOutput = output
    print(maxOutput)

class Amplifier:
    registers = []
    instructionPointer = 0
    output = -1
    input = 0
    phaseSetting = -1
    usePhaseSetting = True
    def __init__(self, puzzleInput, phaseSetting):
        self.registers = puzzleInput.split(',')
        for i, item in enumerate(self.registers):
            self.registers[i] = int(item)
        self.phaseSetting = phaseSetting

    def go(self, newInput):
        self.input = newInput
        nextInput = self.phaseSetting if self.usePhaseSetting else self.input
        while self.registers[self.instructionPointer] != 99:
            parameterModes, opcode, numParameters = interpretInstruction(self.registers[self.instructionPointer])
            parameters = numpy.zeros(numParameters)
            for i in range(numParameters):
                parameters[i] = int(self.registers[self.instructionPointer + i + 1])
            self.instructionPointer, newOutput, switchInput = executeInstruction(parameterModes, opcode, parameters, nextInput, self.registers, self.instructionPointer)
            if switchInput:
                self.usePhaseSetting = False
                nextInput = self.input
            if newOutput != -1:
                self.output = newOutput
                return self.output
        return self.output

def runEverything(puzzleInput, phaseSettings):
    a = Amplifier(puzzleInput, phaseSettings[0])
    b = Amplifier(puzzleInput, phaseSettings[1])
    c = Amplifier(puzzleInput, phaseSettings[2])
    d = Amplifier(puzzleInput, phaseSettings[3])
    e = Amplifier(puzzleInput, phaseSettings[4])
    amplifiers = [a, b, c, d, e]
    currentAmplifier = 0
    mostRecentOutput = 0
    while e.registers[e.instructionPointer] != 99:
        mostRecentOutput = amplifiers[currentAmplifier].go(mostRecentOutput)
        currentAmplifier += 1
        currentAmplifier %= 5
    return e.output

def part2(puzzleInput):
    basicPhaseSettings = [9, 8, 7, 6, 5]
    phaseSettingsList = getAllPhaseSettings(basicPhaseSettings)
    maxOutput = -1
    i = 1
    for phaseSettings in phaseSettingsList:
        #print(phaseSettings)
        #print(i)
        output = runEverything(puzzleInput, phaseSettings)
        #print(output)
        if output > maxOutput:
            maxOutput = output
        i += 1
    print(maxOutput)

f = open("day7input.txt", "r")
puzzleInput = f.read()
f.close()
#puzzleInput = '3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5'

part2(puzzleInput)
