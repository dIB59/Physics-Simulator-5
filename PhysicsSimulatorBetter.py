import math
import pygame
import random
from pygame import gfxdraw

#Need to implement substeps, for more accurate simulation
G = 6.67

class Particle:


    TIMESTEP = 1  #Each time step is 1/2 day

    def __init__(self, x, y, radius, color, mass, name):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.mass = mass
        self.name = name

        self.orbit = []

        self.x_vel = 0
        self.y_vel = 0

    #displays text on screen with a white rectangle
    # def text_objects(text, font):
    #     textSurface = font.render(text, True, (255,255,255))
    #     return textSurface, textSurface.get_rect()

    #Defines the draw function
    def draw(self, win):
        x = self.x
        y = self.y

        #If we have more than 2 points of a partcile's position we will do the following
        if 150 > len(self.orbit) > 2:
            updated_points = []         #Gets a list of updated points which are the x, y coordinates to scale
            for point in self.orbit:
                x, y = point
                updated_points.append((x, y))

            #Takes a list of points and draws lines between those points and does not eclose them
            # because of False
            pygame.draw.aalines(win, self.color, False, updated_points, 2)

            #Remove line after it is drawn after 10 points
            if len(self.orbit) > 100:
                self.orbit.pop(0)

    #def draw_circle(win, self, x, y, radius, color):
        x = self.x
        y = self.y
        #Draws a circle based on the cordinates of the particle and their radius
        
        pygame.draw.circle(win, self.color, (x, y), self.radius)

        #Anti Aliasing the circles
        x_int = int(x)
        y_int = int(y)
        self.radius_int = int(self.radius)

        #OverflowError: signed short integer is less than minimum
        #probably comes from the following 2 lines of code and the above three
        #that are required to make the code work
        gfxdraw.aacircle(win, x_int, y_int, self.radius_int, self.color)
        gfxdraw.filled_circle(win, x_int, y_int, self.radius_int, self.color)

    def circle_surf(radius, color):
        surf = pygame.Surface((radius * 2, radius *2))
        pygame.draw.circle(surf, color, (radius, radius), radius)
        surf.set_colorkey((0,0,0))
        return surf

    def combine_particle(self, other):
        other_x, other_y = other.x, other.y
        distance_x = other_x - self.x
        distance_y = other_y - self.y
        distance = math.sqrt(distance_x ** 2 + distance_y ** 2)

        #to avoid division by zero
        if 2 <= distance:
            for i in range(2):
                x = (self.x + other.x)/2
                y = (self.y + other.y)/2
                color = ((self.color + other.color)/2)
                radius = self.radius + other.radius
                mass = radius * 2
                particleName = self.particleName + other.particleName
                Particle.createdParticles.append(Particle(x, y, radius, color, mass, particleName))
                del Particle.create_particles[self,other]
        return Particle.createdParticles  

    #Calculating the gravitational forces between two particles
    def attraction(self, other):
        #Pythagoras theorem
        other_x, other_y = other.x, other.y
        distance_x = other_x - self.x
        distance_y = other_y - self.y
        distance = math.sqrt(distance_x ** 2 + distance_y ** 2)

        #to avoid division by zero
        if 2 <= distance <= 0:
            distance = 2

        try:

        #Calculating the gravitational forces between two particles
            force = G * (self.mass * other.mass) / distance ** 2

        except ZeroDivisionError:
            force = G * (self.mass * other.mass) / 1

        #atan function -> y over x and gives the angle associated with it
        theta = math.atan2(distance_y, distance_x)

        #force in the x direction and y direction
        force_x = math.cos(theta) * force
        force_y = math.sin(theta) * force
        return force_x, force_y

    #If the particles collide, we will make them bounce off eachother including the radius
    def collision(self, other):
        
        if self.x - self.radius <= other.x + other.radius and self.x + self.radius >= other.x - other.radius:
            if self.y - self.radius <= other.y + other.radius and self.y + self.radius >= other.y - other.radius:
                #Calculate angle of incidence of the collision
                theta = math.atan2(self.y - other.y, self.x - other.x)
                #Calculate the angle of reflection
                theta_reflection = math.pi - theta
                #Calculate the velocity of the particle after the collision
                self.x_vel = math.cos(theta_reflection) * self.x_vel
                self.y_vel = math.sin(theta_reflection) * self.y_vel
                other.x_vel = math.cos(theta_reflection) * other.x_vel
                other.y_vel = math.sin(theta_reflection) * other.y_vel
                #Calculate the new position of the particles after the collision
                self.x = self.x + self.x_vel * Particle.TIMESTEP
                self.y = self.y + self.y_vel * Particle.TIMESTEP
                other.x = other.x + other.x_vel * Particle.TIMESTEP
                other.y = other.y + other.y_vel * Particle.TIMESTEP
                


    #updates the postion of particles besed on the gravcitational force it is effected by
    def update_position(self, particles):

        #Collision between particles
        for particle in particles:
            if particle != self:
                self.collision(particle)

        #gets the screen size (width, height)
        WIDTH, HEIGHT = pygame.display.get_surface().get_size()

        #collision with screen borders (if the particle goes out of bounds)(decreases the speed as well)
        if self.x >= WIDTH or self.x <= 0:
            self.x_vel *= -0.9 
        if self.y >= HEIGHT or self.y <= 0:
            self.y_vel *= -0.9 
        #if the particle is still out of bounds after the collision given some tolerance, it will be reset to the a random point in the screen
        if self.x >= WIDTH + self.radius or self.x <= -self.radius:
            #Set the speed to 0 AND give it new coordinates
            self.x_vel = 0
            self.x = random.randrange(WIDTH) / 2
            self.y = random.randrange(HEIGHT) / 2
        if self.y >= HEIGHT + self.radius or self.y <= -self.radius:
            self.x = random.randrange(WIDTH) / 2
            self.y = random.randrange(HEIGHT) / 2
            self.y_vel = 0
      

        total_fx = total_fy = 0
        for particle in particles:

            if self == particle:
                continue

            fx, fy = self.attraction(particle)
            total_fx += fx
            total_fy += fy

        #Calculate Velocity using a = F / m
        self.x_vel += total_fx / self.mass * self.TIMESTEP
        self.y_vel += total_fy/ self.mass * self.TIMESTEP

        #Because sometimes the velocity is too high and the particle goes off the screen
        #We will make sure that the velocity is not too high

        MAXSPEED = 1

        if self.x_vel > 10 * MAXSPEED:
            print(self.x_vel)
            self.x_vel = self.x_vel * 0.7
        if self.y_vel > 10 * MAXSPEED:
            print(self.y_vel)
            self.y_vel = self.y_vel * 0.7
        if self.x_vel < -10 * 10 * MAXSPEED:
            print(self.x_vel)
            self.x_vel = self.x_vel * 0.7
        if self.y_vel < -10 * MAXSPEED:
            print(self.y_vel)
            self.y_vel = self.y_vel * 0.7

    
        #Update coordinates usuing velocity
        #Timestep is used to ensure the we are moving the accurate amount of time
        self.x += self.x_vel * self.TIMESTEP
        self.y += self.y_vel * self.TIMESTEP
        
        #Append the current position to the orbit list
        self.orbit.append((self.x, self.y))

    #create a list of random particles
    def create_particles(self, num_particles):

        WIDTH, HEIGHT = pygame.display.get_surface().get_size()

        createdParticles = []
        for i in range(num_particles):
            x = random.randint(0, WIDTH)
            y = random.randint(0, HEIGHT)
            color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
            radius = random.randint(3, 9)
            mass = radius * 2
            particleName = "Particle" + str(i)
            createdParticles.append(Particle(x, y, radius, color, mass, particleName))

        return createdParticles

    #def paused():

        clock = pygame.time.Clock()

        WIDTH, HEIGHT = pygame.display.get_surface().get_size()

        largeText = pygame.font.SysFont("comicsansms",115)
        TextSurf, TextRect = text_objects("Paused", largeText)
        TextRect.center = ((WIDTH/2),(HEIGHT/2))

        gameDisplay.blit(TextSurf, TextRect)
        

        while pause:
            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                    
            #gameDisplay.fill(white)
            

            button("Continue",150,450,100,50,green,bright_green,unpause)
            button("Quit",550,450,100,50,red,bright_red,quitgame)

            pygame.display.update()
            clock.tick(15)  

def main():
    
    pygame.init()

    WIDTH, HEIGHT = 1000, 1000

    WIN = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
    pygame.display.set_caption('A particle simulation')

    run = True
    clock = pygame.time.Clock()

    #define particles such that thier radius and mass are the same
    #lpartice = Particle(Spawn x        , spawn y          , RADIUS        , COLOUR                                        , mass           ,particleName)
    #random1 = Particle(randrange(WIDTH), randrange(HEIGHT), randrange(5,10), (randrange(256),randrange(256),randrange(256)), randrange(1,10), "random1")

    #Tells which particles to draw
    #create particles list
    particles = []
    #ask the user to input the number of particles they want to create
    num_particles = int(input("Enter the number of particles: "))
    particles = Particle.create_particles(particles, num_particles)
    print(particles)

    #print the number of particles created and their names
    print("The following particles were created: ")
    for particle in particles:
        print(particle.name, ", Radius", particle.radius, ", Mass", particle.mass)

    while run:
        #Limits the game to 60fps
        clock.tick(60)
        WIN.fill((0, 0, 0))

        #funtion that quits the game
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        #Draws the particles specified in line 58
        for particle in particles:
            particle.update_position(particles)
            particle.draw(WIN)

        pygame.display.update()        

    pygame.quit()

#main()
if __name__ == "__main__":
    main()