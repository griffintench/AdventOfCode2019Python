def part1(input1, input2):
    firstWire = input1.split(',')
    secondWire = input2.split(',')
    cur = [0, 0]
    wireMap = { str(cur): 3 }
    for inst in firstWire:
        amount = int(inst[1:])
        if inst[0] == 'U':
            for i in range(amount):
                cur[1] += 1
                wireMap[str(cur)] = 1
        elif inst[0] == 'D':
            for i in range(amount):
                cur[1] -= 1
                wireMap[str(cur)] = 1
        elif inst[0] == 'R':
            for i in range(amount):
                cur[0] += 1
                wireMap[str(cur)] = 1
        elif inst[0] == 'L':
            for i in range(amount):
                cur[0] -= 1
                wireMap[str(cur)] = 1
    cur = [0, 0]
    for inst in secondWire:
        amount = int(inst[1:])
        if inst[0] == 'U':
            for i in range(amount):
                cur[1] += 1
                if (str(cur) in wireMap and wireMap[str(cur)] == 1):
                    wireMap[str(cur)] = 3
                else:
                    wireMap[str(cur)] = 2
        elif inst[0] == 'D':
            for i in range(amount):
                cur[1] -= 1
                if (str(cur) in wireMap and wireMap[str(cur)] == 1):
                    wireMap[str(cur)] = 3
                else:
                    wireMap[str(cur)] = 2
        elif inst[0] == 'R':
            for i in range(amount):
                cur[0] += 1
                if (str(cur) in wireMap and wireMap[str(cur)] == 1):
                    wireMap[str(cur)] = 3
                else:
                    wireMap[str(cur)] = 2
        elif inst[0] == 'L':
            for i in range(amount):
                cur[0] -= 1
                if (str(cur) in wireMap and wireMap[str(cur)] == 1):
                    wireMap[str(cur)] = 3
                else:
                    wireMap[str(cur)] = 2
    for key, value in wireMap.items():
        if value == 3:
            print(key)
    return 0

def steps(instructions, key):
    cur = [0, 0]
    steps = 0
    for inst in instructions:
        amount = int(inst[1:])
        if inst[0] == 'U':
            for i in range(amount):
                steps += 1
                cur[1] += 1
                if str(cur) == key:
                    return steps
        elif inst[0] == 'D':
            for i in range(amount):
                steps += 1
                cur[1] -= 1
                if str(cur) == key:
                    return steps
        elif inst[0] == 'L':
            for i in range(amount):
                steps += 1
                cur[0] -= 1
                if str(cur) == key:
                    return steps
        elif inst[0] == 'R':
            for i in range(amount):
                steps += 1
                cur[0] += 1
                if str(cur) == key:
                    return steps
                
    return -1

def part2(input1, input2):
    firstWire = input1.split(',')
    secondWire = input2.split(',')
    cur = [0, 0]
    wireMap = { str(cur): 3 }
    for inst in firstWire:
        amount = int(inst[1:])
        if inst[0] == 'U':
            for i in range(amount):
                cur[1] += 1
                wireMap[str(cur)] = 1
        elif inst[0] == 'D':
            for i in range(amount):
                cur[1] -= 1
                wireMap[str(cur)] = 1
        elif inst[0] == 'R':
            for i in range(amount):
                cur[0] += 1
                wireMap[str(cur)] = 1
        elif inst[0] == 'L':
            for i in range(amount):
                cur[0] -= 1
                wireMap[str(cur)] = 1
    cur = [0, 0]
    for inst in secondWire:
        amount = int(inst[1:])
        if inst[0] == 'U':
            for i in range(amount):
                cur[1] += 1
                if (str(cur) in wireMap and wireMap[str(cur)] == 1):
                    wireMap[str(cur)] = 3
                else:
                    wireMap[str(cur)] = 2
        elif inst[0] == 'D':
            for i in range(amount):
                cur[1] -= 1
                if (str(cur) in wireMap and wireMap[str(cur)] == 1):
                    wireMap[str(cur)] = 3
                else:
                    wireMap[str(cur)] = 2
        elif inst[0] == 'R':
            for i in range(amount):
                cur[0] += 1
                if (str(cur) in wireMap and wireMap[str(cur)] == 1):
                    wireMap[str(cur)] = 3
                else:
                    wireMap[str(cur)] = 2
        elif inst[0] == 'L':
            for i in range(amount):
                cur[0] -= 1
                if (str(cur) in wireMap and wireMap[str(cur)] == 1):
                    wireMap[str(cur)] = 3
                else:
                    wireMap[str(cur)] = 2
    lowest = 100000000
    for key, value in wireMap.items():
        if value == 3 and key != '[0, 0]':
            first = steps(firstWire, key)
            second = steps(secondWire, key)
            if first != -1 and second != -1:
                candidate = steps(firstWire, key) + steps(secondWire, key)
                if (candidate < lowest):
                    lowest = candidate
    print(lowest)
    return 0

f = open("day3input.txt", "r")
input1 = f.readline()
input2 = f.readline()
f.close()
#input1 = 'R8,U5,L5,D3'
#input2 = 'U7,R6,D4,L4'
part2(input1, input2)

"""
1064
"""
