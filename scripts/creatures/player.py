import pygame as py
import scripts.engine.renderer as renderer
import scripts.engine.math as math
import scripts.engine.input as input
import scripts.creatures.enity as enity
import scripts.engine.spritesheet as spritesheet
import scripts.ui.hud
import scripts.ui.backpack as backpack

#TODO add sprite animations
#TODO normalize speed


class Player(enity.Entity):
    def __init__(self, position, scene, magic):
        image = spritesheet.spritesheet("assets/creatures/player.png")
        image = image.image_at((0, 0, 16, 16), py.Color(0, 0, 0))
        enity.Entity.__init__(self, position, image, scene)
        self.obj.w = 16
        self.obj.h = 16
        self.updateImage()
        #self.origin = math.Vector2(self.image.get_width() / 2, self.image.get_height())


        self.hud = scripts.ui.hud.Hud(scene)
        self.backpack.makePlayer()
        self.addMagic(magic)

        up = input.keyInput(py.K_w)
        down = input.keyInput(py.K_s)
        left = input.keyInput(py.K_a)
        right = input.keyInput(py.K_d)

        sprint = input.keyInput(py.K_LCTRL)

        byebyeFriction = input.keyInput(py.K_l)
        byebyeFriction.onDown = self.goodbyeFriction

        sprint.onDown = self.sprintToggle

        up.onDown = self.move_up
        down.onDown = self.move_down
        left.onDown = self.move_left
        right.onDown = self.move_right

        up.onUp = self.up_stop
        down.onUp = self.down_stop
        left.onUp = self.left_stop
        right.onUp = self.right_stop

        blastKey = input.keyInput(py.K_q)
        blastKey.onDown = self.chargeBlast
        blastKey.onUp = self.blast

        #self.debug = True

        self.keys = {
            "up": False,
            "down": False,
            "left": False,
            "right": False
        }

        self.sprinting = False
        self.humanoid["speed"] = 1
        self.friction = 0.5

    def blast(self, key):
        if self.magic.isEquipped is True:
            self.magic.blast(math.Vector2(py.mouse.get_pos()[0], py.mouse.get_pos()[1]))
    def chargeBlast(self, key):
        if self.magic.isEquipped is True:
            self.magic.chargeBlast()

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
    def goodbyeFriction(self, key):
        self.friction = 0

    def update(self, dt):
        previousPosition = math.Vector2(self.obj.x, self.obj.y)
        if self.keys["left"] is True:
            self.velocity.x = -self.humanoid["speed"]
        if self.keys["right"] is True:
            self.velocity.x = self.humanoid["speed"]
        if self.keys["up"] is True:
            self.velocity.y = -self.humanoid["speed"]
        if self.keys["down"] is True:
            self.velocity.y = self.humanoid["speed"]

        self.obj.x += self.velocity.x; self.obj.y += self.velocity.y
        if self.velocity.x > 0:
            self.velocity.x -= self.friction
        elif self.velocity.x < 0:
            self.velocity.x += self.friction
        
        if self.velocity.y > 0:
            self.velocity.y -= self.friction
        elif self.velocity.y < 0:
            self.velocity.y += self.friction

        if self.velocity.x >= 0 and self.velocity.x <= 0.2:
            self.velocity.x = 0
        
        if self.velocity.y >= 0 and self.velocity.y <= 0.2:
            self.velocity.y = 0
        
        self.collisionCheck(previousPosition)
        self.humanoid["health"] -= 0.1

        self.pointAt(math.Vector2(py.mouse.get_pos()[0], py.mouse.get_pos()[1]), 9, 5)
    def onUi(self):
        self.hud.update()
        self.backpack.update()

    def stateChange(self, state):
        if state == "normalCharge":
            self.changeImage("assets/creatures/plrEquip2.png")
        elif state == "idle":
            self.changeImage("assets/creatures/player.png")