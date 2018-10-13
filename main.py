from PIL import Image
from swarm import Vec2, PI, Swarm


Width, Height = 1600, 1200


img = Image.new(mode="RGB",
                size=(Width, Height),
                color=(0, 0, 0))

swarm = Swarm(100000)
for particle in swarm:
    img.putpixel((particle.position + Vec2(800, 600)).pixel(), particle.colour)

img.save("image.png")