def part1(input):
    registers = input.split(',')
    for i, item in enumerate(registers):
        registers[i] = int(item)
    registers[1] = 12
    registers[2] = 2
    cur = 0
    while (registers[cur] != 99):
        if (registers[cur] == 1):
            registers[registers[cur + 3]] = registers[registers[cur + 1]] + registers[registers[cur + 2]]
        elif (registers[cur] == 2):
            registers[registers[cur + 3]] = registers[registers[cur + 1]] * registers[registers[cur + 2]]
        cur += 4
    print(registers[0])
    print(registers)

def makeAttempt(input, noun, verb):
    registers = input.split(',')
    for i, item in enumerate(registers):
        registers[i] = int(item)
    registers[1] = noun
    registers[2] = verb
    cur = 0
    while (cur < len(registers) and registers[cur] != 99):
        if cur + 3 >= len(registers):
            return -1
        if registers[cur + 1] >= len(registers):
            return -1
        if (registers[cur + 2] >= len(registers)):
            return -1
        if (registers[cur + 3] >= len(registers)):
            return -1
        if (registers[cur] == 1):
            registers[registers[cur + 3]] = registers[registers[cur + 1]] + registers[registers[cur + 2]]
        elif (registers[cur] == 2):
            registers[registers[cur + 3]] = registers[registers[cur + 1]] * registers[registers[cur + 2]]
        else:
            return -1
        cur += 4
    if (cur >= len(registers)):
        return -1
    return registers[0]

def part2(input):
    noun = 0
    verb = 0
    limit = len(input.split(','))
    # limit = 2
    while noun < limit:
        while verb < limit:
            # print(str(noun) + " " + str(verb) + ":" + str(makeAttempt(input, noun, verb)))
            if makeAttempt(input, noun, verb) == 19690720:
                print(100 * noun + verb)
                return
            verb += 1
        noun += 1
        verb = 0
    print("Failed :(")

f = open("day2input.txt", "r")
input = f.read()
f.close()
testInput = "1,1,1,4,99,5,6,0,99"
part2(input)
