import pygame as py
import scripts.ui.backpack as backpack
import scripts.engine.renderer as renderer
import scripts.engine.math as math

class Magic(backpack.tool):
    def __init__(self, wielder):
        backpack.tool.__init__(self)
        self.wielder = wielder
        self.colour = py.Color(0, 0, 0)
        self.magicCircle = None

    def blast(self, position):
        print(position)
    def chargeBlast(self):
        pass

    def createNormalMagicCircle(self):
        self.magicCircle = renderer.object(math.Vector2(self.wielder.obj.x, self.wielder.obj.y), self.wielder.scene)
        self.magicCircle.zIndex = self.wielder.zIndex
        self.magicCircle.colour = self.colour
        self.magicCircle.obj.w = 60
        self.magicCircle.obj.h = 5
    def update(self):
        if self.magicCircle is not None:
            self.magicCircle.setPos(self.wielder.obj.x, self.wielder.obj.y)

class Fire(Magic):
    def __init__(self, wielder):
        Magic.__init__(self, wielder)
        self.Icon = "assets/tools/fireMagicIcon.png"
        self.colour = py.Color(237, 124, 31)
    def blast(self, position):
        self.wielder.stateChange("idle")
        self.magicCircle.destroy()
        print(position)
    def chargeBlast(self):
        self.wielder.stateChange("normalCharge")
        self.createNormalMagicCircle()
        