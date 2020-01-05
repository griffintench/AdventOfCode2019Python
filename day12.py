import bisect
import numpy

class Moon:
    velX = 0
    velY = 0
    velZ = 0
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
    def move(self):
        self.x += self.velX
        self.y += self.velY
        self.z += self.velZ
    def applyGravity(self, other):
        if other.x > self.x:
            self.velX += 1
        elif other.x < self.x:
            self.velX -= 1
        if other.y > self.y:
            self.velY += 1
        elif other.y < self.y:
            self.velY -= 1
        if other.z > self.z:
            self.velZ += 1
        elif other.z < self.z:
            self.velZ -= 1
    def getEnergy(self):
        return (abs(self.x) + abs(self.y) + abs(self.z)) * (abs(self.velX) + abs(self.velY) + abs(self.velZ))
    def getState(self):
        return self.x * 115856201 + self.y * 2825761 + self.z * 68921 + self.velX * 1681 + self.velY * 41 + self.velZ

def index(a, x):
    i = bisect.bisect_left(a, x)
    if i != len(a) and a[i] == x:
        return i
    return -1

def part1(io, europa, ganymede, callisto):
    moons = [io, europa, ganymede, callisto]
    for i in range(1000):
        for moon in moons:
            for other in moons:
                if moon != other:
                    moon.applyGravity(other)
        for moon in moons:
            moon.move()
    totalEnergy = 0
    for moon in moons:
        totalEnergy += moon.getEnergy()
    print(totalEnergy)

def getTotalState(moons, callisto):
    totalState = 0
    for moon in moons:
        if moon != callisto:
            totalState *= 37
            totalState += moon.getState()
    return totalState

class State:
    def __init__(self, planet1, planet2, planet3):
        self.x1 = planet1.x
        self.y1 = planet1.y
        self.z1 = planet1.z
        self.velX1 = planet1.velX
        self.velY1 = planet1.velY
        self.velZ1 = planet1.velZ
        self.x2 = planet2.x
        self.y2 = planet2.y
        self.z2 = planet2.z
        self.velX2 = planet2.velX
        self.velY2 = planet2.velY
        self.velZ2 = planet2.velZ
        self.x3 = planet3.x
        self.y3 = planet3.y
        self.z3 = planet3.z
        self.velX3 = planet3.velX
        self.velY3 = planet3.velY
        self.velZ3 = planet3.velZ

    def isEqual(self, other):
        if self.x1 != other.x1 or self.y1 != other.y1 or self.z1 != other.z1:
            return False
        if self.velX1 != other.velX1 or self.velY1 != other.velY1 or self.velZ1 != other.velZ1:
            return False
        if self.x2 != other.x2 or self.y2 != other.y2 or self.z2 != other.z2:
            return False
        if self.velX2 != other.velX2 or self.velY2 != other.velY2 or self.velZ2 != other.velZ2:
            return False
        if self.x3 != other.x3 or self.y3 != other.y3 or self.z3 != other.z3:
            return False
        if self.velX3 != other.velX3 or self.velY3 != other.velY3 or self.velZ3 != other.velZ3:
            return False
        return True

def isStateDuplicate(state, states):
    for s in states:
        if s.isEqual(state):
            return True
    return False

class OneDimensionMoon:
    vel = 0
    def __init__(self, crd):
        self.crd = crd

    def move(self):
        a = self.crd
        b = self.vel
        self.crd += self.vel

    def applyGravity(self, other):
        a = self.crd
        b = self.vel
        c = other.crd
        if other.crd > self.crd:
            self.vel += 1
        elif other.crd < self.crd:
            self.vel -= 1

def compareLists(l1, l2):
    if len(l1) != len(l2):
        return False
    for i in range(len(l1)):
        if l1[i] != l2[i]:
            return False
    return True

def getOneDimension(ioCrd, europaCrd, ganymedeCrd, callistoCrd):
    io = OneDimensionMoon(ioCrd)
    europa = OneDimensionMoon(europaCrd)
    ganymede = OneDimensionMoon(ganymedeCrd)
    callisto = OneDimensionMoon(callistoCrd)
    originalState = [ioCrd, 0, europaCrd, 0, ganymedeCrd, 0]
    i = 0
    moons = [io, europa, ganymede, callisto]
    while True: # lol who needs good code
        if i % 1000000 == 0:
            print('round: ' + str(i))
        for moon in moons:
            for other in moons:
                if moon != other:
                    moon.applyGravity(other)
        for moon in moons:
            moon.move()
        state = [io.crd, io.vel, europa.crd, europa.vel, ganymede.crd, ganymede.vel]
        i += 1
        if compareLists(originalState, state):
            return i

def actualPart2(io, europa, ganymede, callisto):
    print('starting x...')
    x = getOneDimension(io.x, europa.x, ganymede.x, callisto.x)
    print('starting y...')
    y = getOneDimension(io.y, europa.y, ganymede.y, callisto.y)
    print('starting z...')
    z = getOneDimension(io.z, europa.z, ganymede.z, callisto.z)
    print(x)
    print(y)
    print(z)
    print(numpy.lcm.reduce([x, y, z]))

def part2(io, europa, ganymede, callisto):
    moons = [io, europa, ganymede, callisto]
    originalState = State(io, europa, ganymede)
    i = 0
    while True:
        if i % 1000000 == 0:
            print('round: ' + str(i))
        state = State(io, europa, ganymede)
        if originalState.isEqual(state) and i != 0:
            print(i)
            return
        for moon in moons:
            if moon != callisto:
                for other in moons:
                    if moon != other:
                        moon.applyGravity(other)
        for moon in moons:
            if moon != callisto:
                moon.move()
        callisto.x = -1 * (io.x + europa.x + ganymede.x)
        callisto.y = -1 * (io.y + europa.y + ganymede.y)
        callisto.z = -1 * (io.z + europa.z + ganymede.z)
        callisto.velX = -1 * (io.velX + europa.velX + ganymede.velX)
        callisto.velY = -1 * (io.velY + europa.velY + ganymede.velY)
        callisto.velZ = -1 * (io.velZ + europa.velZ + ganymede.velZ)
        i += 1
        

# no external input for this one, hard-coding the values

io = Moon(17, -12, 13)
europa = Moon(2, 1, 1)
ganymede = Moon(-1, -17, 7)
callisto = Moon(12, -14, 18)

#io = Moon(-1, 0, 2)
#europa = Moon(2, -10, -7)
#ganymede = Moon(4, -8, 8)
#callisto = Moon(3, 5, -1)

actualPart2(io, europa, ganymede, callisto)
