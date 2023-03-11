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

# define a Quadtree class to store and manipulate the spheres
class Quadtree:
    def __init__(self, bounds, capacity):
        self.bounds = bounds  # the bounding rectangle of the quadtree
        self.capacity = capacity  # the maximum number of spheres per node
        self.spheres = []  # the spheres in this quadtree node
        self.divided = False  # whether this node has been divided into sub-nodes

    def subdivide(self):
        # calculate the dimensions of the sub-nodes
        x = self.bounds[0]
        y = self.bounds[1]
        w = self.bounds[2] / 2
        h = self.bounds[3] / 2

        # create the four sub-nodes
        top_left = (x, y, w, h)
        top_right = (x + w, y, w, h)
        bottom_left = (x, y + h, w, h)
        bottom_right = (x + w, y + h, w, h)

        # create the four sub-nodes and store them in a list
        self.nodes = [
        Quadtree(top_left, self.capacity),
        Quadtree(top_right, self.capacity),
        Quadtree(bottom_left, self.capacity),
        Quadtree(bottom_right, self.capacity)
        ]
        self.divided = True

def insert(self, sphere):
    # if this node has been divided, insert the sphere into the appropriate sub-node
    index = -1
    if self.divided:
        index = self.get_index(sphere)
    if index != -1:
        self.nodes[index].insert(sphere)
        return

    # otherwise, add the sphere to this node's list of spheres
    self.spheres.append(sphere)

    # if this node's sphere list is at capacity, divide the node
    if len(self.spheres) > self.capacity:
        if not self.divided:
            self.subdivide()

    # move any spheres in this node's list into the appropriate sub-node
    if self.divided:
        i = 0
        while i < len(self.spheres):
            index = self.get_index(self.spheres[i])
            if index != -1:
                self.nodes[index].insert(self.spheres[i])
                self.spheres.pop(i)
            else:
                i += 1


        # otherwise, add the sphere to this node's list of spheres
        self.spheres.append(sphere)

        # if this node's sphere list is at capacity, divide the node
        if len(self.spheres) > self.capacity:
            if not self.divided:
                self.subdivide()

        # move any spheres in this node's list into the appropriate sub-node
        if self.divided:
            for i in range(len(self.spheres)):
                index = self.get_index(self.spheres[i])
            if index != -1:
                self.nodes[index].insert(self.spheres[i])
                self.spheres.pop(i)

def query(self, bounds):
        # create a list to store the spheres in the specified bounds
        spheres = []

        # if this node doesn't intersect the bounds, return an empty list
        if not self.intersects(bounds):
            return spheres

        # add any spheres in this node's list to the list
        for sphere in self.spheres:
            if bounds.contains(sphere):
                spheres.append(sphere)

        # if this node has been divided, add any spheres in the sub-nodes to the list
        if self.divided:
            for node in self.nodes:
                spheres.extend(node.query(bounds))

        # return the list of spheres
        return spheres