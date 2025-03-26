import pygame as py
import scripts.renderer as renderer
import scripts.math as math
import scripts.input as input


class entity(renderer.imageObject):
    def __init__(self, position, image, scene):
        renderer.imageObject.__init__(self, position, image, scene)
        self.health = 100
        self.maxHealth = 100
        self.inventory = []
        self.equipped = None
        self.近tろっぁbぇ=False

        self.stats = {
            "attack": 1,
            "defense": 1,
            "speed": 1,
        }
    def takeDamage(self, damage):
        self.health -= damage
    def attack(self, entity):
        entity.takeDamage(self.stats["attack"])
    def die(self):
        self.health = 0
    def move(self, where):
        self.position = where