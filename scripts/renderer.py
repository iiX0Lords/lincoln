import pygame as py
import scripts.input as input
import scripts.math as math


class scene:
    def __init__(self):
        self.objects = []
        self.camera = camera()

    def render(self, screen):
        for obj in self.objects:
            if obj.ui == False:
                obj.render(screen)
        for obj in self.objects:
            if obj.ui == True:
                obj.render(screen)

class object:
    def __init__(self, position, scene):
        self.obj = py.Rect(position.x, position.y, 10, 10)
        self.colour = py.Color(255, 255, 255)
        self.scene = scene
        self.ui = False
        self.scene.objects.append(self)
        self.width = 0

    def render(self, screen):
        renderRect = py.Rect()
        renderPos = math.Vector2(self.obj.x, self.obj.y).toScreenSpace(self.scene.camera, screen)
        renderRect.update(renderPos.x, renderPos.y, self.obj.w, self.obj.h)

        py.draw.rect(screen, self.colour, renderRect, width=self.width)

    def destroy(self):
        self.scene.objects.remove(self)

class imageObject(object):
    def __init__(self, position, image, scene):
        self.image = py.image.load(image).convert_alpha()
        object.__init__(self, position, scene)

    def scale(self, newSize):
        self.image = py.transform.scale(self.image, newSize)
        self.obj.w = self.image.get_width()
        self.obj.h = self.image.get_height()

    def changeImage(self, newImage):
        old = self.image.get_size()
        self.image = py.image.load(newImage).convert_alpha()
        self.scale(math.Vector2(old[0], old[1]))

    def render(self, screen):
        renderPos = math.Vector2(self.obj.x, self.obj.y).toScreenSpace(self.scene.camera, screen)
        screen.blit(self.image, (renderPos.x, renderPos.y))

class frame(object):
    def __init__(self, position, scene):
        object.__init__(self, position, scene)
        self.ui = True

class button(frame):
    def __init__(self, position, scene):
        frame.__init__(self, position, scene)
        self.hovering = False

        self.buttonEvent = input.mouseInput(1)
        self.buttonEvent.onDown = self.checkOn
        self.buttonEvent.onUp = self.checkOff

    def checkOn(self, key):
        pos = math.Vector2(py.mouse.get_pos()[0], py.mouse.get_pos()[1]).toWorldSpace(self.scene.camera, py.display.get_surface())
        if self.obj.collidepoint(pos.x, pos.y):
            self.onPress(self)
    def checkOff(self, key):
        pos = math.Vector2(py.mouse.get_pos()[0], py.mouse.get_pos()[1]).toWorldSpace(self.scene.camera, py.display.get_surface())
        if self.obj.collidepoint(pos.x, pos.y):
            self.onUp(self)

    def onPress(self, why = None):
        pass
    def onUp(self, why = None):
        pass
    def onHover(self, why = None):
        pass
    def onUnhover(self, why = None):
        pass
    def destroy(self):
        self.scene.objects.remove(self)
        self.buttonEvent.unregisterKey()

class camera():
    def __init__(self):
        self.position = math.Vector2(py.display.get_surface().get_width() / 2, py.display.get_surface().get_height() / 2)
        self.zoom = 1