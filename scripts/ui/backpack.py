
import pygame as py
import scripts.engine.input as input
import scripts.engine.renderer as renderer

tools = [None, None, None, None]

class tool:
    def __init__(self):
        self.Icon = None
        self.active = False
        self.isEquipped = False

    def equipped(self):
        pass

    def unequipped(self):
        pass

    def activated(self):
        pass
    
    def update(self):
        pass

class hotbarIcon:
    def __init__(self, index, scene):
        self.index = index
        self.scene = scene
        self.icon = renderer.imageFrame(py.Vector2(0,0), "assets/hud/toolbar.png", self.scene)
        self.icon.obj.w = 20
        self.icon.obj.h = 20
        self.icon.updateImage()
        self.icon.obj.y = (600 - self.icon.obj.h) - 15
        self.icon.obj.x = 210 + (self.icon.obj.w + ( (self.icon.obj.w + 10) * self.index))

        self.toolIcon = renderer.imageFrame(py.Vector2(0,0), "assets/hud/toolbar.png", self.scene)
        self.toolIcon.obj.w = 10
        self.toolIcon.obj.h = 10
        self.toolIcon.zIndex = 1
        self.toolIcon.updateImage()
        self.toolIcon.obj.x = self.icon.obj.x + self.toolIcon.obj.w / 2
        self.toolIcon.obj.y = self.icon.obj.y + self.toolIcon.obj.h / 2

        self.text = renderer.textLabel(py.Vector2(0,0), "", "assets/fonts/pixel.ttf", self.scene)
        self.text.zIndex = 105
        self.text.textSize = 15
        self.text.text = str(self.index + 1)

        self.text.obj.x = self.icon.obj.x + 8
        self.text.obj.y = self.icon.obj.y + 8

        self.wasNone = True
        self.justEquipped = False

        
    def update(self, equipped):
        if tools[self.index] is not None:
            tl = tools[self.index]

            if self.wasNone is True:
                self.wasNone = False
                if tl.Icon is not None:
                    self.toolIcon.changeImage(tl.Icon)
            
            if equipped is not None and self.justEquipped is False:
                self.justEquipped = True
                self.icon.changeImage("assets/hud/toolbarEquipped.png")
                

            if tl.Icon is not None:
                self.toolIcon.zIndex = 100
        else:
            self.wasNone = True

class backpack:
    def __init__(self, scene):
        self.isPlayer = False
        self.scene = scene
        self.equipped = None
        self.hotbar = [None,None,None,None]

    def makePlayer(self):
        self.inputs = [input.keyInput(py.K_1), input.keyInput(py.K_2), input.keyInput(py.K_3), input.keyInput(py.K_4)]
        for key in self.inputs:
            key.onDown = self.inputHandler
            key.onUp = self.inputHandlerUp

        for i in range(len(self.inputs)):
            self.hotbar[i] = hotbarIcon(i, self.scene)
        self.isPlayer = True

    def inputHandler(self, key):
        if key == self.inputs[0]:
            if tools[0] is not None:
                if self.equipped == tools[0]:
                    self.equipped.unequipped()
                    self.equipped.isEquipped = False
                    self.equipped = None
                else:
                    self.equipped = tools[0]
                    tools[0].equipped()
        elif key == self.inputs[1]:
            if tools[1] is not None:
                if self.equipped == tools[1]:
                    self.equipped.unequipped()
                    self.equipped.isEquipped = False
                    self.equipped = None
                else:
                    self.equipped = tools[1]
                    tools[1].equipped()
        elif key == self.inputs[2]:
            if tools[2] is not None:
                if self.equipped == tools[2]:
                    self.equipped.unequipped()
                    self.equipped.isEquipped = False
                    self.equipped = None
                else:
                    self.equipped = tools[2]
                    tools[2].equipped()
        elif key == self.inputs[3]:
            if tools[3] is not None:
                if self.equipped == tools[3]:
                    self.equipped.unequipped()
                    self.equipped.isEquipped = False
                    self.equipped = None
                else:
                    self.equipped = tools[3]
                    tools[3].equipped()

    def inputHandlerUp(self, key):
        pass

    def onUi(self):
        pass

    def addTool(self, tool, index):
        tools[index] = tool

    def update(self):
        if self.isPlayer is True:
            for icon in self.hotbar:
                icon.update(self.equipped)

            if self.equipped is not None:
                self.equipped.update()
                self.equipped.isEquipped = True

                if py.mouse.get_pressed()[0] is True:
                    if self.equipped.active is False:
                        self.equipped.activated()
                        self.equipped.active = True
                else:
                    self.equipped.active = False
            else:
                for icon in self.hotbar:
                        if icon.justEquipped is True:
                            icon.justEquipped = False
                            icon.icon.changeImage("assets/hud/toolbar.png")