
import pygame as py
import scripts.engine.math as math
import scripts.engine.renderer as renderer

class Hud:
    def __init__(self, scene):
        self.scene = scene
        thumbnail = renderer.imageFrame(math.Vector2(8, 12), py.image.load("assets/hud/thumbnail.png"), scene)
        thumbnail.obj.w = 40
        thumbnail.obj.h = 40
        thumbnail.updateImage()
        self.thumbnail = thumbnail

        healthBar = renderer.imageFrame(math.Vector2(135, 26), py.image.load("assets/hud/emptybar.png"), scene)
        healthBar.obj.w = 75
        healthBar.obj.h = 6
        healthBar.updateImage()
        self.healthBar = healthBar

        healthBg = renderer.frame(math.Vector2(135, 26), scene)
        healthBg.colour = py.Color(200, 0, 0)
        healthBg.obj.w = healthBar.obj.w
        healthBg.obj.h = healthBar.obj.h
        healthBg.zIndex = 97

        health = renderer.frame(math.Vector2(135, 26), scene)
        health.colour = py.Color(0, 255, 0)
        health.obj.w = healthBar.obj.w
        health.obj.h = healthBar.obj.h
        health.zIndex = 98
        self.health = health

        energyBar = renderer.imageFrame(math.Vector2(135, 50), py.image.load("assets/hud/emptybar.png"), scene)
        energyBar.obj.w = 50
        energyBar.obj.h = 6
        energyBar.updateImage()
        self.energyBar = energyBar

        energyBg = renderer.frame(math.Vector2(135, 50), scene)
        energyBg.colour = py.Color(0, 38, 110)
        energyBg.obj.w = energyBar.obj.w
        energyBg.obj.h = energyBar.obj.h
        energyBg.zIndex = 97

        energy = renderer.frame(math.Vector2(135, 50), scene)
        energy.colour = py.Color(0, 88, 255)
        energy.obj.w = energyBar.obj.w
        energy.obj.h = energyBar.obj.h
        energy.zIndex = 98
        self.energy = energy

    def update(self):
        playerHealth = self.scene.player.humanoid["health"]
        maxHealth = self.scene.player.humanoid["maxHealth"]
        energyStat = self.scene.player.humanoid["energy"]
        maxEnergy = self.scene.player.humanoid["maxEnergy"]

        healthWidth = (playerHealth / maxHealth) * self.healthBar.obj.w
        self.health.obj.w = healthWidth

        energyWidth = (energyStat / maxEnergy) * self.energyBar.obj.w
        self.energy.obj.w = energyWidth

