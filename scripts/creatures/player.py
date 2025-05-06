import pygame as py
import scripts.engine.renderer as renderer
import scripts.engine.math as math
import scripts.engine.input as input
import scripts.creatures.enity as enity
import scripts.engine.spritesheet as spritesheet
import pytmx

#TODO add sprite animations
#TODO normalize speed
#TODO change movement to use velocity based instead so it is smoother w friction

class Player(enity.Entity):
    def __init__(self, position, scene):
        image = spritesheet.spritesheet("assets/creatures/player.png")
        image = image.image_at((0, 0, 16, 16), py.Color(0, 0, 0))
        enity.Entity.__init__(self, position, image, scene)
        self.obj.w = 16
        self.obj.h = 16

        up = input.keyInput(py.K_w)
        down = input.keyInput(py.K_s)
        left = input.keyInput(py.K_a)
        right = input.keyInput(py.K_d)

        sprint = input.keyInput(py.K_LCTRL)

        sprint.onDown = self.sprintToggle

        up.onDown = self.move_up
        down.onDown = self.move_down
        left.onDown = self.move_left
        right.onDown = self.move_right

        up.onUp = self.up_stop
        down.onUp = self.down_stop
        left.onUp = self.left_stop
        right.onUp = self.right_stop

        self.keys = {
            "up": False,
            "down": False,
            "left": False,
            "right": False
        }

        self.sprinting = False
        self.humanoid["speed"] = 1

    def move_left(self, key):
        self.keys["left"] = True
    def move_right(self, key):
        self.keys["right"] = True
    def move_up(self, key):
        self.keys["up"] = True
    def move_down(self, key):
        self.keys["down"] = True

    def left_stop(self, key):
        self.keys["left"] = False
    def right_stop(self, key):
        self.keys["right"] = False
    def up_stop(self, key):
        self.keys["up"] = False
    def down_stop(self, key):
        self.keys["down"] = False
    
    def sprintToggle(self, key):
        self.sprinting = not self.sprinting
        if self.sprinting:
            self.humanoid["speed"] = 2
        else:
            self.humanoid["speed"] = 1
    
    def update(self, dt):
        if self.keys["left"] == True:
            self.obj.x -= self.humanoid["speed"]
        if self.keys["right"] == True:
            self.obj.x += self.humanoid["speed"]
        if self.keys["up"] == True:
            self.obj.y -= self.humanoid["speed"]
        if self.keys["down"] == True:
            self.obj.y += self.humanoid["speed"]
    
        tile_x = int(self.obj.x // 16)
        tile_y = int(self.obj.y // 16)

        tile = self.scene.mapGrid[tile_x][tile_y]
        if tile:
            self.zIndex = tile.zIndex + 1