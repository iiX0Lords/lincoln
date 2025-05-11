import pygame as py
import scripts.engine.renderer as renderer
import scripts.engine.math as math
import scripts.engine.input as input

zones = []

class zone():
    def __init__(self, zone, map):
        self.map = map
        self.mapGrid = [[None for _ in range(self.map.width)] for _ in range(self.map.height)]
        self.mapTiles = []
        self.active = False
        self.obj = zone
        zones.append(self)

    def isInside(self, position):
        x, y = self.obj.x, self.obj.y
        w, h = self.obj.width, self.obj.height

        if position.x > x and position.x < x + w and position.y > y and position.y < y + h:
            return True
        return False