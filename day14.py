import numpy

def getIngredients(map, product):
    for key, value in map.items():
        if key[1] == product:
            return value, key[0]
    print('product not found: ' + product)
    return [], key[0]

def getOreNeeded(map, product, spareIngredients, amount):
    baseIngredients, producesAmount = getIngredients(map, product)
    multiple = numpy.ceil(amount / producesAmount)
    ingredients = []
    for baseIngredient in baseIngredients:
        ingredients.append((multiple * baseIngredient[0], baseIngredient[1]))
    oreNeeded = 0
    for ingredient in ingredients:
        if ingredient[1] == 'ORE':
            oreNeeded += ingredient[0]
        elif spareIngredients[ingredient[1]] >= ingredient[0]:
            spareIngredients[ingredient[1]] -= ingredient[0]
        else:
            amountNeeded = ingredient[0] - spareIngredients[ingredient[1]]
            spareIngredients[ingredient[1]] = 0
            oreNeeded += getOreNeeded(map, ingredient[1], spareIngredients, amountNeeded)
    spareIngredients[product] += multiple * producesAmount - amount
    return oreNeeded

def part1(map):
    spareIngredients = {}
    for key in map.keys():
        spareIngredients[key[1]] = 0
    ingredients = getIngredients(map, 'FUEL')
    print(getOreNeeded(map, 'FUEL', spareIngredients, ingredients[1]))

def initSpareIngredients(map):
    spareIngredients = {}
    for key in map.keys():
        spareIngredients[key[1]] = 0
    return spareIngredients

def part2(map):
    oreInventory = 1000000000000
    floor = 1
    ceiling = 1000000000000
    while floor != ceiling - 1:
        testValue = (ceiling + floor) // 2
        spareIngredients = initSpareIngredients(map)
        oreNeeded = getOreNeeded(map, 'FUEL', spareIngredients, testValue)
        if oreNeeded > oreInventory:
            ceiling = testValue
        else:
            floor = testValue
    print(floor)

map = {}
f = open("day14input.txt", "r")
for line in f:
    if line[-1] == '\n':
        line = line[:-1]
    splitLine = line.split(' => ')
    ingredients = splitLine[0]
    product = splitLine[1]
    splitIngredients = ingredients.split(', ')
    splitProduct = product.split(' ')
    productTuple = (int(splitProduct[0]), splitProduct[1])
    ingredientsList = []
    for ingredient in splitIngredients:
        splitIngredient = ingredient.split(' ')
        ingredientsList.append((int(splitIngredient[0]), splitIngredient[1]))
    map[productTuple] = ingredientsList
f.close()

part2(map)
