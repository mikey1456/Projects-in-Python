############################
#   First-Year Project:    #
#   Adaptation of Osmos    #
#                          #
############################


import simplegui, random, math

CANVAS_WIDTH = 500
CANVAS_HEIGHT = 500

NUM_ENEMIES = 10
NUM_ORBS = 20
ORB_RADIUS = 2

def randCol():
    r = random.randrange (0, 256)
    g = random.randrange (0, 256)
    b = random.randrange (0, 256)
    return 'rgb('+str(r)+ ','+str(g)+ ','+str(b)+ ')'
ORB_COLOUR = randCol()

def randPos():
    x = random.randrange (0, CANVAS_WIDTH)
    y = random.randrange (0, CANVAS_HEIGHT)
    return Vector(x, y)

def randVel():
    x = random.randrange (-3, 3)
    y = random.randrange (-3, 3)
    return Vector(x, y)

class Vector:

    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

   
    def __str__(self):
        return "(" + str(self.x) + "," + str(self.y) + ")"

   
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

   
    def __ne__(self, other):
        return not self.__eq__(other)

   
    def get_p(self):
        return (self.x, self.y)

   
    def copy(self):
        return Vector(self.x, self.y)

   
    def add(self, other):
        self.x += other.x
        self.y += other.y
        return self

    def __add__(self, other):
        return self.copy().add(other)

   
    def negate(self):
        return self.multiply(-1)

    def __neg__(self):
        return self.copy().negate()

 
    def subtract(self, other):
        return self.add(-other)

    def __sub__(self, other):
        return self.copy().subtract(other)

   
    def multiply(self, k):
        self.x *= k
        self.y *= k
        return self

    def __mul__(self, k):
        return self.copy().multiply(k)

    def __rmul__(self, k):
        return self.copy().multiply(k)

   
    def divide(self, k):
        return self.multiply(1/k)

    def __truediv__(self, k):
        return self.copy().divide(k)

 
    def normalize(self):
        return self.divide(self.length())

    def get_normalized(self):
        return self.copy().normalize()


    def dot(self, other):
        return self.x * other.x + self.y * other.y

   
    def length(self):
        return math.sqrt(self.x**2 + self.y**2)

    def length_squared(self):
        return self.x**2 + self.y**2

    def reflect(self, normal):
        n = normal.copy()
        n.multiply(2*self.dot(normal))
        self.subtract(n)
        return self

    def angle(self, other):
        return math.acos(self.dot(other) / (self.length() * other.length()))

    def rotate_anti(self):
        self.x, self.y = -self.y, self.x
        return self

    def rotate_rad(self, theta):
        rx = self.x * math.cos(theta) - self.y * math.sin(theta)
        ry = self.x * math.sin(theta) + self.y * math.cos(theta)
        self.x, self.y = rx, ry
        return self
   
    def rotate(self, theta):
        theta_rad = theta / 180 * math.pi
        return self.rotate_rad(theta_rad)
   
    def get_proj(self, vec):
        unit = vec.get_normalized()
        return unit.multiply(self.dot(unit))
       

class Game:

    def __init__(self, clock, interaction, player, enemies, orbs):
        self.clock = clock
        self.interaction = interaction
        self.player = player
        self.enemies = enemies
        self.orbs = orbs
        self.balls = [player] + [enemies] + [orbs]
   
    def draw(self, canvas):
        clock.tick()
        for ball in self.balls:
            ball.draw(canvas)
        interaction.update()
        ball.update()
       

# To-Do
class Interaction:
   
    def __init__(self,player,keyboard):
        self.player=player
        self.keyboard=keyboard # Help from Oliver
       
   
    def update(self):# Help from Oliver
        if self.keyboard.right:
            self.player.vel.add(Vector(1, 0))
        if self.keyboard.left:
            self.player.vel.add(Vector(-1, 0))
        if self.keyboard.up:
            self.player.vel.add(Vector(0, -1))
        if self.keyboard.down:
            self.player.vel.add(Vector(0, 1))
        if self.keyboard.space:
            self.player.vel.multiply(1.1)
               

class Ball:
   
    def __init__(self, pos, vel, radius, colour=None):
        self.pos = pos
        self.vel = vel
        self.radius = radius
        if colour is None:
            self.colour = randCol()
        else:
            self.colour = colour
       
    def update(self):
        self.pos = self.pos.add(self.vel)
        self.vel.multiply(0.85)
       
    def hit(self, ball):
        pass
       
    def draw(self, canvas):
        self.update()
        canvas.draw_circle(self.pos.get_p(), self.radius, 1, self.colour,  self.colour)

       
class Player(Ball):
   
    def __init__(self):
        super().__init__(Vector(CANVAS_WIDTH/2, CANVAS_HEIGHT/2), Vector(0,0), 10, colour='White')
       

class Enemy(Ball):
   
    def __init__(self):
        super().__init__(randPos(), randVel(), 10)
       
    def update(self):
        global clock
        if clock.transition(30):
            self.vel = randVel()
        self.pos = self.pos.add(self.vel)


class Orb(Ball):
   
    def __init__(self):
        super().__init__(randPos(), Vector(0,0), ORB_RADIUS, colour=ORB_COLOUR)
       
# To-Do        
class Obstacle(Ball):
   
    def __init__(self):
        super().__init__(20)

class Keyboard:
    def __init__(self):
        self.right=False
        self.left=False
        self.up=False
        self.down=False
        self.space=False
     
    def keyDown(self, key): # With help from Oliver
        if key == simplegui.KEY_MAP['right']:
            self.right = True
        if key == simplegui.KEY_MAP['left']:
            self.left = True
        if key == simplegui.KEY_MAP['up']:
            self.up = True
        if key == simplegui.KEY_MAP['down']:
            self.down = True
        if key == simplegui.KEY_MAP['space']:
            self.space = True

    def keyUp(self, key): # With help from Oliver
        if key == simplegui.KEY_MAP['right']:
            self.right = False
        if key == simplegui.KEY_MAP['left']:
            self.left = False
        if key == simplegui.KEY_MAP['up']:
            self.up = False
        if key == simplegui.KEY_MAP['down']:
            self.down = False
        if key == simplegui.KEY_MAP['space']:
            self.space = False
           
   
class Clock:
   
    def __init__(self):
        self.time = 0
       
    def tick(self):
        self.time += 1
       
    def transition(self, duration):
        return (self.time % duration == 0)

   
#From Tom:
# Setup for the game should go below.
# Any objects that you intended to use more than once can be put into lists.
#
# Next steps for you to take:
#
# - You should create the player object and the enemy, orb and obstacle objects.
# - You will need a Game object to keep track of the state of the game and rest of the objects.
#   - It takes a Clock, Interaction and Player objects
#   - It should also take lists of Enemy, Orb and Obstacle objects.
# - Your Interaction class should also have a reference to the ball objects as it needs to check
#   for collisions etc.
# - You should create any other classes you may need too.

clock=Clock()
keyboard=Keyboard()
player=Player()
interaction=Interaction(player, keyboard)
enemies=Enemy()
orbs=Orb()
game = Game(clock, interaction, player, enemies, orbs)


frame = simplegui.create_frame("Osmos", CANVAS_WIDTH, CANVAS_HEIGHT)
# Frame handler is expecting to be set to the draw method of your Game object.
frame.set_draw_handler(game.draw)
frame.set_keydown_handler(keyboard.keyDown)
frame.set_keyup_handler(keyboard.keyUp)
frame.start()
