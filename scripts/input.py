import pygame as py

keys = []
mouses = []
class keyInput:
    def __init__(self, keycode):
        self.keycode = keycode
        self.isDown = False
        keys.append(self)
    def onDown(self, why = None):
        pass
    def onUp(self, why = None):
        pass
    def unregisterKey(self):
        keys.remove(self)

class mouseInput:
    def __init__(self, mouseBtn):
        self.mouseBtn = mouseBtn
        self.isDown = False
        mouses.append(self)
    def onDown(self, why = None):
        pass
    def onUp(self, why = None):
        pass
    def unregisterKey(self):
        mouses.remove(self)


def handleInput(event):

    if event.type == py.KEYDOWN:
        for key in keys:
            if event.key == key.keycode:
                key.onDown(key)
    elif event.type == py.KEYUP:
        for key in keys:
            if event.key == key.keycode:
                key.onUp(key)
    elif event.type == py.MOUSEBUTTONDOWN:
        for mouse in mouses:
            if event.button == mouse.mouseBtn:
                mouse.onDown(mouse)
    elif event.type == py.MOUSEBUTTONUP:
        for mouse in mouses:
            if event.button == mouse.mouseBtn:
                mouse.onUp(mouse)
        