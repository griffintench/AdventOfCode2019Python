def part1(input1, input2):
    count = 0
    for i in range(input1, input2):
        stri = str(i)
        adjacent = False
        nonDecreasing = True
        for j in range(5):
            if stri[j + 1] == stri[j]:
                adjacent = True
            if stri[j + 1] < stri[j]:
                nonDecreasing = False
        if adjacent and nonDecreasing:
            count += 1
    print(count)
    return 0

def part2(input1, input2):
    count = 0
    for i in range(input1, input2):
        stri = str(i)
        adjacent = False
        adjacentCount = 1
        for j in range(5):
            if stri[j + 1] == stri[j]:
                if adjacentCount == 0:
                    adjacentCount = 1
                elif adjacentCount == 1:
                    adjacentCount = 2
                    adjacent = True
                else:
                    adjacentCount += 1
                    adjacent = False
            else:
                if adjacentCount == 2:
                    adjacent = True
                    break
                else:
                    adjacentCount = 1
        nonDecreasing = True
        for j in range(5):
            if stri[j + 1] < stri[j]:
                nonDecreasing = False
        if adjacent and nonDecreasing:
            count += 1
    print(count)
    return 0

#f = open("day4input.txt", "r")
#input = f.read()
#f.close()
input1 = 402328
input2 = 864247
#input1 = 223444
#input2 = input1 + 1

part2(input1, input2)
