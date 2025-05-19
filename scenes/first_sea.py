import pygame as py
import scripts.engine.renderer as renderer
import scripts.engine.math as vector2
import math
import scripts.engine.input as input
import pytmx.util_pygame as tiledPygame
import pytmx
import scripts.zones as zoneManager
import scripts.creatures.player as player

spawns = []

def handleObjects(obj):
    if obj.data.properties["spawner"]:
          print(obj.data.properties["spawner"])
          spawns.append(obj)

def is_integer(s):
    try:
        int(s)
        return True
    except ValueError:
        return False
    

#TODO add save file
class first_sea(renderer.scene):
    def __init__(self):
        renderer.scene.__init__(self)
        self.active = True

        self.map = tiledPygame.load_pygame("assets/maps/first_sea.tmx")

        self.camera.zoom = 3

        self.player = player.Player(vector2.Vector2(0, 0), self, "Fire")
        self.player.zIndex = 2
        self.mapGrid = [[None for _ in range(self.map.width)] for _ in range(self.map.height)]
        self.mapTiles = []
        self.zones = []

        for obj in self.map.get_layer_by_name("zones"):
            self.zones.append(zoneManager.zone(obj, self.map))

        for layer in self.map:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, image in layer.tiles():
                    if layer.name != "Water" :
                        obj = renderer.imageObject(vector2.Vector2(x * 16, y * 16), image, self)
                        obj.layer = layer.name
                        obj.zIndex = 1
                        if layer.name == "Decorations":
                             obj.zIndex = 2
                        #self.mapGrid[x][y] = obj
                        #self.mapTiles.append(obj)
                        obj.updateImage()
                        #obj.debug = True

                        for zone in self.zones:
                            if zone.isInside(obj.obj):
                                zone.mapTiles.append(obj)
                                zone.mapGrid[x][y] = obj
            elif isinstance(layer, pytmx.TiledObjectGroup):
                if layer.name != "zones":
                    for obj in self.map.get_layer_by_name(layer.name):
                        if obj is not None:
                            if obj.image is not None:
                                objI = renderer.imageObject(vector2.Vector2(obj.x, obj.y), obj.image, self)
                                objI.layer = layer.name
                                objI.data = obj
                                objI.zIndex = int(layer.name)
                                objI.updateImage()
                                handleObjects(objI)

    
        self.player.setPos(spawns[0].obj.x, spawns[0].obj.y)
    def update(self, dt):
        self.camera.position = self.camera.position.lerp(vector2.Vector2(self.player.obj.x, self.player.obj.y), 0.1)
        self.player.update(dt)
        self.player.onUi()
        
        for zone in self.zones:
            x, y = zone.obj.x, zone.obj.y
            w, h = zone.obj.width, zone.obj.height

            if self.player.obj.x > x and self.player.obj.x < x + w and self.player.obj.y > y and self.player.obj.y < y + h:
                zone.active = True
                self.player.currentZone = zone
            else:
                zone.active = False
                self.player.currentZone = None

    def events(self, event):
        if event.type == py.MOUSEMOTION:
            pass