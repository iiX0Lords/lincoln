import pygame as py
import scripts.ui.backpack as backpack
import scripts.engine.renderer as renderer
import math as pymath
import scripts.engine.math as math

class Magic(backpack.tool):
    def __init__(self, wielder):
        backpack.tool.__init__(self)
        self.wielder = wielder
        self.colour = py.Color(0, 0, 0)
        self.magicCircle = None

    def blast(self, position):
        self.wielder.stateChange("idle")
        self.magicCircle.destroy()
    def chargeBlast(self):
        self.wielder.stateChange("normalCharge")
        self.createNormalMagicCircle()

    def createNormalMagicCircle(self):
        self.magicCircle = renderer.object(math.Vector2(self.wielder.obj.x, self.wielder.obj.y), self.wielder.scene)
        self.magicCircle.zIndex = self.wielder.zIndex
        self.magicCircle.colour = self.colour
        self.magicCircle.obj.w = 60
        self.magicCircle.obj.h = 5
    def update(self):
        if self.magicCircle is not None:
            angle = self.wielder.angle
            
            self.magicCircle.rotation = angle - 90
            self.magicCircle.setPos(self.wielder.obj.x, self.wielder.obj.y)
            self.magicCircle.moveForward(9, angle)


class Fire(Magic):
    def __init__(self, wielder):
        Magic.__init__(self, wielder)
        self.Icon = "assets/tools/fireMagicIcon.png"
        self.colour = py.Color(237, 124, 31)
    def blast(self, position):
        Magic.blast(self, position)
        fireBall = renderer.animatedImage(py.Rect(0, 0, 32, 31), self.wielder.scene, "assets/magic/fire/fireBall.png", 8)
        fireBall.zIndex = self.wielder.zIndex
        fireBall.obj.x = self.wielder.obj.x - 16
        fireBall.obj.y = self.wielder.obj.y - 16

        fireBall.angle = self.wielder.angle
        rotatedImage, newRect = fireBall.rot_center(fireBall.image, self.wielder.angle, fireBall.obj.w/2, fireBall.obj.h/2)
        fireBall.rotated = rotatedImage

        fireBall.obj.x = self.wielder.obj.x - newRect.centerx + fireBall.obj.w/2
        fireBall.obj.y = self.wielder.obj.y - newRect.centery + fireBall.obj.h/2

        mousePos = math.Vector2(position.x, position.y).toWorldSpace(self.wielder.scene.camera, py.display.get_surface())
        playerPos = math.Vector2(self.wielder.obj.x, self.wielder.obj.y)
        direction = (mousePos - playerPos).normalize()
        fireBall.friction = 1
        fireBall.velocity = direction * 4
    def chargeBlast(self):
        Magic.chargeBlast(self)
        