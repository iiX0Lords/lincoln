import pygame as py
import scripts.engine.input as input
import math as pymath
import scripts.engine.math as math
import scripts.engine.spritesheet as spritesheet

scenes = []

class scene:
    def __init__(self):
        self.objects = []
        self.camera = camera()
        self.active = False
        scenes.append(self)

    def render(self, screen):
        sortedObjects = sorted(self.objects, key=lambda obj: obj.zIndex)
        for obj in sortedObjects:
            if obj.ui is False:
                obj.render(screen)
        for obj in sortedObjects:
            if obj.ui is True:
                obj.render(screen)
                obj.update()
    def update(self, dt):
        pass

class object:
    def __init__(self, position, scene):
        self.obj = py.Rect(position.x, position.y, 10, 10)
        self.colour = py.Color(255, 255, 255)
        self.scene = scene
        self.ui = False
        self.scene.objects.append(self)
        self.width = 0
        self.zIndex = 0
        self.rotation = None

    def renderRotated(self, position, screen):
        x,y = position.x, position.y
        width, height = self.obj.w, self.obj.h
        rotation = self.rotation
        points = []
        radius = pymath.sqrt((height / 2)**2 + (width / 2)**2)
        angle = pymath.atan2(height / 2, width / 2)
        angles = [angle, -angle + pymath.pi, angle + pymath.pi, -angle]
        rotRadians = (pymath.pi / 180) * rotation

        for angle in angles:
            yOffset = -1 * radius * pymath.sin(angle + rotRadians)
            xOffset = radius * pymath.cos(angle + rotRadians)
            points.append((x + xOffset, y + yOffset))

        py.draw.polygon(screen, self.colour, points)

    def moveForward(self, amount, angle = None):
        if angle is None:
            angle = self.rotation
        x = amount * pymath.cos(pymath.radians(angle))
        y = -amount * pymath.sin(pymath.radians(angle))
        x = self.obj.x + x
        y = self.obj.y + y
        self.setPos(x, y)

    def render(self, screen):
        if self.ui is False:
            renderRect = py.Rect()
            renderPos = math.Vector2(self.obj.x, self.obj.y).toScreenSpace(self.scene.camera, screen)
            if self.rotation is not None:
                self.renderRotated(renderPos, screen)
            else:
                renderRect.update(renderPos.x, renderPos.y, self.obj.w, self.obj.h)
                py.draw.rect(screen, self.colour, renderRect, width=self.width)
        else:
            if self.rotation is not None:
                self.renderRotated(math.Vector2(self.obj.x, self.obj.y), screen)
            else:
                py.draw.rect(screen, self.colour, self.obj, width=self.width)
    def setPos(self, x, y):
        self.obj.x = x
        self.obj.y = y

    def destroy(self):
        self.scene.objects.pop(self.scene.objects.index(self))

class imageObject(object):
    def __init__(self, position, image, scene):
        if type(image) == str:
            self.image = py.image.load(image).convert_alpha()
        else:
            self.image = image.convert_alpha()
        object.__init__(self, position, scene)
        self.debug = False
        self.debugColour = py.Color(255, 0, 0)
        self.origin = math.Vector2()#math.Vector2(self.image.get_width() / 2, self.image.get_height() / 2)
        self.obj = self.returnNewRect()
        self.rotated = None

    def returnNewRect(self):
        return self.image.get_rect(x=self.obj.x, y=self.obj.y)

    def scale(self, newSize):
        self.image = py.transform.scale(self.image, newSize)
        self.obj = self.returnNewRect()

    def changeImage(self, newImage):
        old = self.image.get_size()
        self.image = py.image.load(newImage).convert_alpha()
        self.scale(math.Vector2(old[0], old[1]))

    def updateImage(self):
        self.image = py.transform.scale(self.image, math.Vector2(self.obj.w * self.scene.camera.zoom, self.obj.h * self.scene.camera.zoom))
        self.obj = self.returnNewRect()
        self.origin = math.Vector2()#math.Vector2(self.image.get_width() / 2, self.image.get_height() / 2)

    def render(self, screen):
        renderPos = math.Vector2(self.obj.x, self.obj.y).toScreenSpace(self.scene.camera, screen)
        renderPos -= self.origin
        if renderPos.x < screen.get_width() and renderPos.y < screen.get_height():
            if renderPos.x + self.image.get_width() > 0 and renderPos.y + self.image.get_height() > 0:
                if self.rotated != None:
                    screen.blit(self.rotated, (renderPos.x - self.rotated.get_width() / 2, renderPos.y - self.rotated.get_height() / 2))
                else:
                    screen.blit(self.image, (renderPos.x, renderPos.y))

        if self.debug is True:
            position = math.Vector2(self.obj.x, self.obj.y)
            position = position.toScreenSpace(self.scene.camera, py.display.get_surface())
            debugRect = py.Rect(position.x, position.y, 5, 5)
            py.draw.rect(py.display.get_surface(), self.debugColour, debugRect)

            renderRect = py.Rect()
            renderPos = math.Vector2(self.obj.x, self.obj.y).toScreenSpace(self.scene.camera, screen)
            renderRect.x = renderPos.x; renderRect.y = renderPos.y
            renderRect.w = self.obj.w; renderRect.h = self.obj.h

            py.draw.rect(screen, self.debugColour, renderRect, 2, 1)


class imageObjectSpritesheet(object):
    def __init__(self, position, spriteposition, size, gridPos, scene):
        object.__init__(self, position, scene)
        self.spritesheet = spritesheet.spritesheet("assets/tiles/iso.png")
        self.gridPos = gridPos
        self.image = self.spritesheet.image_at((spriteposition.x, spriteposition.y, size.x, size.y), py.Color(0, 0, 0))
        self.image = self.image.convert_alpha()
    def scale(self, newSize):
        self.image = py.transform.scale(self.image, newSize)
        self.obj.w = self.image.get_width()
        self.obj.h = self.image.get_height()

    def changeImage(self, spriteposition, size):
        old = self.image.get_size()
        self.image = self.spritesheet.image_at((spriteposition.x, spriteposition.y, size.x, size.y), py.Color(0, 0, 0))
        self.scale(math.Vector2(old[0], old[1]))
        self.image = self.image.convert_alpha()

    def render(self, screen):
        cart_x = self.gridPos.x * 42
        cart_y = self.gridPos.y * 42
        iso_x = (cart_x - cart_y) 
        iso_y = (cart_x + cart_y)/2

        renderPos = math.Vector2(iso_x, iso_y)
        renderPos = renderPos.toScreenSpace(self.scene.camera, screen)
        screen.blit(self.image, (renderPos.x, renderPos.y))

class camera():
    def __init__(self):
        self.position = math.Vector2(py.display.get_surface().get_width() / 2, py.display.get_surface().get_height() / 2)
        self.zoom = 1

class frame(object):
    def __init__(self, position, scene):
        object.__init__(self, position, scene)
        self.zIndex = 99
        self.ui = True
    def update(self):
        pass

class imageFrame(imageObject):
    def __init__(self, position, image, scene):
        imageObject.__init__(self, position, image, scene)
        self.zIndex = 99
        self.ui = True
    def render(self, screen):
        if self.rotated is not None:
            screen.blit(self.rotated, (self.obj.x - self.rotated.get_width() / 2, self.obj.y - self.rotated.get_height() / 2))
        else:
            screen.blit(self.image, (self.obj.x, self.obj.y))
    def update(self):
        pass

class button(imageFrame):
    def __init__(self, position, image, scene):
        imageFrame.__init__(self, position, image, scene)
        self.hovering = False

    def onClick(self, position):
        pass
    def onUnclick(self, position):
        pass
    def onHover(self, position):
        pass
    def onUnhover(self, position):
        pass

    def update(self):
        mousePosition = math.Vector2(py.mouse.get_pos()[0], py.mouse.get_pos()[1])
        if self.obj.collidepoint(mousePosition):
            self.hovering = True
            self.onHover(mousePosition)
        else:
            if self.hovering is True:
                self.hovering = False
                self.onUnhover(mousePosition)

        if self.hovering is True:
            if py.mouse.get_pressed()[0] is True:
                self.onClick(mousePosition)
            else:
                self.onUnclick(mousePosition)


class textLabel(frame):
    def __init__(self, position, text, fontFile, scene):
        frame.__init__(self, position, scene)
        self.text = text
        self.oldText = text
        self.textObj = None

        self.fontFile = fontFile
        self.textSize = 20
        self.backgroundColour = None

        self.updateFont()

    def updateFont(self):
        self.font = py.font.Font(self.fontFile, self.textSize)

        if self.textObj is not None:
            oldPosition = math.Vector2(self.obj.x, self.obj.y)
            oldSize = math.Vector2(self.obj.h, self.obj.w)

            self.textObj = self.font.render(self.text, True, self.colour, self.backgroundColour)
            self.obj = self.textObj.get_rect()

            self.obj.x = oldPosition.x
            self.obj.y = oldPosition.y

            self.obj.w = oldSize.x
            self.obj.h = oldSize.y
        else:
            self.textObj = self.font.render(self.text, True, self.colour, self.backgroundColour)
            self.obj = self.textObj.get_rect()

    def update(self):
        if self.oldText != self.text:
            self.oldText = self.text
            self.updateFont()

    def render(self, screen):
        screen.blit(self.textObj, self.obj)