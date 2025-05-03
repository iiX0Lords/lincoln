import pygame as py
import scripts.engine.renderer as renderer
import scripts.engine.math as math
import scripts.engine.input as input
import scripts.zones as zoneManager


class Entity(renderer.imageObject):
    def __init__(self, position, image, scene):
        renderer.imageObject.__init__(self, position, image, scene)
        self.stats = {
            "energy": 0,
            "mp": 0,
            "str": 0,
        }
        self.humanoid = {
            "health": 100,
            "maxHealth": 100,
            "speed": 1
        }
        self.ai = False
    def takeDamage(self, amount):
        self.stats["health"] -= amount
    def heal(self, amount):
        self.stats["health"] += amount