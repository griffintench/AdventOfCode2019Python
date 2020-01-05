
def howManyOrbits(input, object):
    if object not in input:
        return 0
    else:
        return 1 + howManyOrbits(input, input[object])

def part1(input):
    orbits = 0
    for key in input.keys():
        orbits += howManyOrbits(input, key)
    print(orbits)

def part2(input):
    start = input['YOU']
    end = input['SAN']
    min = {}
    for key in input.keys():
        min[key] = -1
    min['COM'] = -1
    min[start] = 0
    while min[end] == -1:
        for key, value in min.items():
            if key != 'COM' and value != -1:
                if min[input[key]] == -1:
                    min[input[key]] = 1 + value
            if key != 'COM' and value == -1:
                if min[input[key]] != -1:
                    min[key] = 1 + min[input[key]]
    print(min[end])

f = open("day6input.txt", "r")
input = {}
for line in f:
    if line[-1] == '\n':
        line = line[:-1]
    objects = line.split(')')
    input[objects[1]] = objects[0]
f.close()
part2(input)
