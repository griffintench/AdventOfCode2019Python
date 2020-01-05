def part1(input):
    width = 25
    height = 6
    imageSize = width * height
    layers = []
    while len(input) != 0:
        layer = input[:imageSize]
        layers.append(layer)
        input = input[imageSize:]
    fewestZeroDigits = 9999999999999999
    correctLayer = 0
    for i, layer in enumerate(layers):
        zeroCount = 0
        for c in layer:
            if c == '0':
                zeroCount += 1
        if zeroCount < fewestZeroDigits:
            fewestZeroDigits = zeroCount
            correctLayer = i
    ones = 0
    twos = 0
    for c in layers[correctLayer]:
        if c == '1':
            ones += 1
        elif c == '2':
            twos += 1
    print(ones * twos)
    return

width = 25
height = 6

def getLayers(input):
    imageSize = width * height
    layers = []
    while len(input) != 0:
        layer = input[:imageSize]
        layers.append(layer)
        input = input[imageSize:]
    return layers

def part2(input):
    layers = getLayers(input)
    for y in range(height):
        row = ""
        for x in range(width):
            i = 0
            while i < len(layers) and layers[i][width * y + x] == '2':
                i += 1
            if i == len(layers):
                row += '2'
            else:
                row += layers[i][width * y + x]
        print(row)

f = open("day8input.txt", "r")
input = f.read()
f.close()

#input = '0222112222120000'
part2(input)
