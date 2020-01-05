import math

def part1():
    f = open("day1input.txt", "r")
    total = 0
    for line in f:
        fuel = int(line)
        fuel /= 3
        fuel = math.floor(fuel)
        fuel -= 2
        total += fuel
    print(total)
    f.close()

def fuel(mass):
    nextLevel = math.floor(mass / 3) - 2
    if (nextLevel <= 0):
        return 0
    return nextLevel + fuel(nextLevel)

def part2():
    f = open("day1input.txt", "r")
    total = 0
    for line in f:
        total += fuel(int(line))
    f.close()
    print(total)

part2()
