from PIL import Image
from swarm import Vec2, PI


Width, Height = 800, 600


img = Image.new(mode="RGB",
                size=(Width, Height),
                color=(0, 0, 0))


vec = Vec2(100, 0)

for i in range(10000):
    img.putpixel((vec + Vec2(400, 300)).pixel(), (255, 255, 255))
    vec = vec.rotate(0.0001 * 2 * PI)

vec *= 1.1

for i in range(10000):
    img.putpixel((vec + Vec2(400, 300)).pixel(), (255, 255, 255))
    vec = vec.rotate(0.0001 * 2 * PI)

img.save("image.png")