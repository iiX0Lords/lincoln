
import pygame as py
import scripts.engine.input as input
import scripts.engine.renderer as renderer

tools = [None, None, None, None]

class tool:
    def __init__(self):
        self.Icon = None

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

        self.wasNone = True

        
    def update(self):
        if tools[self.index] is not None:
            tl = tools[self.index]

            if self.wasNone is True:
                self.wasNone = False
                if tl.Icon is not None:
                    self.toolIcon.changeImage(tl.Icon)

            if tl.Icon is not None:
                self.toolIcon.zIndex = 100
        else:
            self.wasNone = True

class backpack:
    def __init__(self, scene):
        self.scene = scene
        self.inputs = [input.keyInput(py.K_1), input.keyInput(py.K_2), input.keyInput(py.K_3), input.keyInput(py.K_4)]
        self.equipped = None
        self.hotbar = [0,0,0,0]
        for key in self.inputs:
            key.onDown = self.inputHandler
            key.onUp = self.inputHandlerUp

        for i in range(len(self.inputs)):
            self.hotbar[i] = hotbarIcon(i, self.scene)

    def inputHandler(self, key):
        if key == self.inputs[0]:
            if tools[0] is not None:
                if self.equipped == tools[0]:
                    self.equipped.unequipped()
                    self.equipped = None
                else:
                    self.equipped = tools[0]
                    tools[0].equipped()
        elif key == self.inputs[1]:
            if tools[1] is not None:
                if self.equipped == tools[1]:
                    self.equipped.unequipped()
                    self.equipped = None
                else:
                    self.equipped = tools[1]
                    tools[1].equipped()
        elif key == self.inputs[2]:
            if tools[2] is not None:
                if self.equipped == tools[2]:
                    self.equipped.unequipped()
                    self.equipped = None
                else:
                    self.equipped = tools[2]
                    tools[2].equipped()
        elif key == self.inputs[3]:
            if tools[3] is not None:
                if self.equipped == tools[3]:
                    self.equipped.unequipped()
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
        print("Inserted new tool")

    def update(self):

        for icon in self.hotbar:
            icon.update()

        if self.equipped is not None:
            self.equipped.update()

            if py.mouse.get_pressed()[0] is True:
                self.equipped.activated()