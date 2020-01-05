def parseInput(input):
    x = 0
    y = 0
    asteroids = []
    for c in input:
        if c == '\n':
            y += 1
            x = 0
        else:
            if c == '#':
                asteroids.append((x, y))
            x += 1
    return asteroids

def getSlopesDict(source, asteroids):
    slopes = {}
    for asteroid in asteroids:
        if source != asteroid:
            if asteroid[0] == source[0]:
                if asteroid[1] > source[1]:
                    if '+inf' not in slopes:
                        slopes['+inf'] = 0
                    slopes['+inf'] += 1
                else:
                    if '-inf' not in slopes:
                        slopes['-inf'] = 0
                    slopes['-inf'] += 1
            else:
                slope = (asteroid[1] - source[1]) / (asteroid[0] - source[0])
                slope = round(slope, 5)
                if asteroid[0] < source[0]:
                    slope = '+' + str(slope)
                else:
                    slope = '-' + str(slope)
                if slope not in slopes:
                    slopes[slope] = 0
                slopes[slope] += 1
    return slopes

def numberOfDetections(source, asteroids):
    return len(getSlopesDict(source, asteroids))

def getMostDetections(asteroids):
    mostDetections = 0
    mostDetectionsAsteroid = asteroids[0]
    for asteroid in asteroids:
        detections = numberOfDetections(asteroid, asteroids)
        if detections > mostDetections:
            mostDetections = detections
            mostDetectionsAsteroid = asteroid
    return mostDetections, mostDetectionsAsteroid

def part1(input):
    asteroids = parseInput(input)
    mostDetections = getMostDetections(asteroids)
    print(mostDetections)

def getAdvancedSlopesDict(source, asteroids):
    minusSlopes = {}
    plusSlopes = {}
    for asteroid in asteroids:
        if source != asteroid:
            if asteroid[0] == source[0]:
                if asteroid[1] > source[1]:
                    if 'inf' not in plusSlopes:
                        plusSlopes['inf'] = []
                    plusSlopes['inf'].append(asteroid)
                else:
                    if 'inf' not in minusSlopes:
                        minusSlopes['inf'] = []
                    minusSlopes['inf'].append(asteroid)
            else:
                slope = (asteroid[1] - source[1]) / (asteroid[0] - source[0])
                slope = round(slope, 5)
                if asteroid[0] < source[0]:
                    slope = str(slope)
                    if slope not in plusSlopes:
                        plusSlopes[slope] = []
                    plusSlopes[slope].append(asteroid)
                else:
                    slope = str(slope)
                    if slope not in minusSlopes:
                        minusSlopes[slope] = []
                    minusSlopes[slope].append(asteroid)
    return minusSlopes, plusSlopes

def part2(input):
    asteroids = parseInput(input)
    mostDetections, asteroid = getMostDetections(asteroids)
    minusSlopes, plusSlopes = getAdvancedSlopesDict(asteroid, asteroids)
    print('minusSlopes: ' + str(len(minusSlopes)))
    print('plusSlopes: ' + str(len(plusSlopes)))
    print('plusinf: ' + str(len(plusSlopes['inf'])))
    vapourized = 0
    # find 154th in plusSlopes ignoring inf
    plusSlopes.pop('inf')
    keys = []
    for key in plusSlopes.keys():
        keys.append(key)
    keys.sort()
    key = keys[153]
    closest = plusSlopes[key][0]
    closestDistance = 10000000
    for candidate in plusSlopes[key]:
        distance = abs(candidate[1] - asteroid[1]) + abs(candidate[0] - asteroid[0])
        if distance < closestDistance:
            closestDistance = distance
            closest = candidate
    print(closest)

f = open("day10input.txt", "r")
input = f.read()
f.close()

part2(input)
