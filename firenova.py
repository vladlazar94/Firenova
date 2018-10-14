import math
import random
from PIL import Image
import os
from pathos.multiprocessing import ProcessingPool as Pool

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

    def translate(self, x, y):
        return Vec2(self.x + x, self.y + y)

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
        self.turn = random.uniform(-1, 1)

    def __str__(self):
        return "position: {}, velocity: {}, colour: {}".format(self.position,
                                                               self.velocity,
                                                               self.colour)


class Swarm:
    def __init__(self, count):
        self.count = count
        self.particles = []

        for _ in range(count):
            norm = random.uniform(0.2, 100)
            angle = random.uniform(0, 2 * PI)

            x = norm * math.cos(angle)
            y = norm * math.sin(angle)

            red = int(random.uniform(0, 255))
            green = int(random.uniform(0, 255))
            blue = int(random.uniform(0, 255))

            position = Vec2(0, 0)
            velocity = Vec2(x, y)
            colour = (red, green, blue)

            self.particles.append(Particle(position, velocity, colour))

    def __iter__(self):
        for particle in self.particles:
            yield particle

    def update(self, interval):
        for particle in self.particles:
            particle.position += particle.velocity * interval
            particle.velocity = particle.velocity.rotate(interval * particle.turn)


class Picture:
    def __init__(self, width, height):
        self.count = 0
        self.width = width
        self.height = height
        self.background = 0, 0, 0

    def size(self):
        return self.width, self.height

    def box_blur(self, image):
        new_img = Image.new("RGB", self.size(), self.background)

        for x in range(self.width):
            for y in range(self.height):
                r, g, b, count = 0, 0, 0, 0

                for i in [-1, 0, 1]:
                    for j in [-1, 0, 1]:
                        if (0 <= x + i < self.width) and (0 <= y + j < self.height):
                            pixel = image.getpixel((x + i, y + j))
                            count += 1
                            r += pixel[0]
                            g += pixel[1]
                            b += pixel[2]

                r, g, b = r // count, g // count, b // count
                new_img.putpixel((x, y), (r, g, b))

        return new_img

        # Broken parallel code:

        # def blur_pixel(pixel):
        #     nonlocal new_img
        #     nonlocal new_img
        #
        #     x, y = pixel[0], pixel[1]
        #
        #     for x in range(self.width):
        #         for y in range(self.height):
        #             r, g, b, count = 0, 0, 0, 0
        #
        #             for i in [-1, 0, 1]:
        #                 for j in [-1, 0, 1]:
        #                     if (0 <= x + i < self.width) and (0 <= y + j < self.height):
        #                         pixel = image.getpixel((x + i, y + j))
        #                         count += 1
        #                         r += pixel[0]
        #                         g += pixel[1]
        #                         b += pixel[2]
        #
        #             r, g, b = r // count, g // count, b // count
        #             new_img.putpixel((x, y), (r, g, b))
        #
        # pixels = []
        # for x in range(self.width):
        #     for y in range(self.height):
        #         pixels.append((x, y))
        #
        # pool = Pool()
        # pool.map(blur_pixel, pixels)
        #
        # return new_img

    def capture(self, swarm, previous=None):
        if previous:
            img = previous
        else:
            img = Image.new("RGB", self.size(), self.background)

        for particle in swarm:
            width, height = particle.position.translate(self.width / 2, self.height / 2).pixel()
            if (0 <= width < self.width) and (0 <= height < self.height):
                img.putpixel((width, height), particle.colour)

        img = self.box_blur(img)
        return img

    def film(self, swarm, frames):
        img = self.capture(swarm)

        for i in range(frames):
            if i % (frames // 100) is 0:
                print("{}%".format(i // (frames // 100)))

            img = self.capture(swarm, img)

            self.count += 1
            if self.count // 10 is 0:
                label = "00" + str(self.count)
            elif self.count // 100 is 0:
                label = "0" + str(self.count)
            else:
                label = str(self.count)

            img.save("./captures/swarm{}.png".format(label))
            swarm.update(0.03)

        print("100%")


os.system("mkdir captures")
os.system("rm out.mp4")

pic = Picture(300, 400)
swarm = Swarm(700)
pic.film(swarm, 100)

os.system("ffmpeg -framerate 30 -pattern_type glob -i 'captures/*.png' -c:v libx264 -r 30 -pix_fmt yuv420p out.mp4")
os.system("rm -rf captures/")




