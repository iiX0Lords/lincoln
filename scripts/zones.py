import pygame as py
import scripts.engine.renderer as renderer
import scripts.engine.math as math
import scripts.engine.input as input

zones = []

class zone():
    def __init__(self, zone):
        self.objects = []
        self.active = False
        self.obj = zone
        zones.append(self)