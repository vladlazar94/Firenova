import math
import random

PI = 3.1415926


class Vec2:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Vec2(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vec2(self.x - other.x, self.y - other.y)

    def __mul__(self, value):
        return Vec2(value * self.x, value * self.y)

    def __getitem__(self, item):
        if item == 0:
            return self.x
        elif item == 1:
            return self.y
        else:
            raise IndexError

    def __str__(self):
        return str((self.x, self.y))

    def pixel(self):
        return int(self.x), int(self.y)

    def norm(self):
        return math.sqrt(self.x ** 2 + self.y ** 2)

    def angle(self):
        x, y = self.x, self.y

        if (x is 0) and (y is 0):
            return 0

        elif (x > 0) and (y is 0):
            return 0

        elif (x > 0) and (y > 0):
            return math.atan(y/x)

        elif (x is 0) and (y > 0):
            return PI/2

        elif (x < 0) and (y > 0):
            return PI - math.atan(-y/x)

        elif (x < 0) and (y is 0):
            return PI

        elif (x < 0) and (y < 0):
            return PI + math.atan(y/x)

        elif (x is 0) and (y < 0):
            return 3 * PI / 2

        elif (x > 0) and (y < 0):
            return 2 * PI + math.atan(y/x)

    def rotate(self, angle):
        new_angle = self.angle() + angle
        return Vec2(self.norm() * math.cos(new_angle),
                    self.norm() * math.sin(new_angle))


class Particle:
    def __init__(self, position, velocity, colour=(255, 255, 255)):
        self.position = position
        self.velocity = velocity
        self.colour = colour

    def update(self, interval):
        self.position += interval * self.velocity


class Swarm:
    def __init__(self, count):
        self.count = count
        self.particles = []

        for _ in range(count):
            norm = random.uniform(0, 400)
            angle = random.uniform(0, 2 * PI)

            x = norm * math.cos(angle)
            y = norm * math.sin(angle)

            red = int(random.uniform(0, 255))
            green = int(random.uniform(0, 255))
            blue = int(random.uniform(0, 255))

            colour = (red, green, blue)

            position = Vec2(x, y)
            velocity = Vec2(0, 0)

            self.particles.append(Particle(position, velocity, colour))

    def __iter__(self):
        for particle in self.particles:
            yield particle