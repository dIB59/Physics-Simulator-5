import pygame
from pygame.math import Vector2

# define the colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# create the pygame window
pygame.init()
size = (700, 500)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Sphere Collision")

# define the Inertia class from the previous example
class Inertia:
  def __init__(self, mass, moment_of_inertia):
    self.mass = mass
    self.moment_of_inertia = moment_of_inertia

  def get_inertia(self):
    return self.mass * self.moment_of_inertia

# define the Sphere class from the previous example
class Sphere:
  def __init__(self, radius, mass):
    self.radius = radius
    self.mass = mass
    self.inertia = Inertia(self.mass, self.radius**2)

    # set initial position and velocity
    self.position = Vector2(0, 0)
    self.velocity = Vector2(0, 0)

  def get_momentum(self):
    return self.mass * self.velocity

  def collide(self, other):
    # calculate the total momentum of the two spheres
    total_momentum = self.get_momentum() + other.get_momentum()

    # calculate the new velocity of each sphere after the collision
    self.velocity = total_momentum / self.mass
    other.velocity = total_momentum / other.mass

    # adjust the position of each sphere to ensure they don't overlap
    self.position += self.radius
    other.position -= other.radius

# create two spheres
sphere1 = Sphere(10, 5)
sphere2 = Sphere(20, 10)

# set the initial position and velocity of each sphere
sphere1.position = Vector2(100, 100)
sphere1.velocity = Vector2(5, 5)
sphere2.position = Vector2(300, 300)
sphere2.velocity = Vector2(-5, -5)

# define the game loop
done = False
while not done:
  # check for user input
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      done = True

  # update the position and velocity of each sphere
  sphere1.position += sphere1.velocity
  sphere2.position += sphere2.velocity

  # check if the spheres have collided
  distance = (sphere1.position - sphere2.position).length()
  if distance < sphere1.radius + sphere2.radius:
    sphere1.collide(sphere2)

  # clear the screen
  screen.fill(BLACK)

  # draw the spheres
  pygame.draw.circle(screen, WHITE, sphere1.position, sphere1.radius)
  pygame.draw.circle(screen, WHITE, sphere2.position, sphere2.radius)

  

  # update the display
pygame.display.update() 
