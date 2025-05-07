import pygame as py
import scripts.engine.renderer as renderer
import scripts.engine.math as math
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


#TODO fix layer issues with map in tiled
#TODO add zone support with updating
#TODO add save file
class first_sea(renderer.scene):
    def __init__(self):
        renderer.scene.__init__(self)
        self.active = True

        self.map = tiledPygame.load_pygame("assets/maps/first_sea.tmx")

        self.camera.zoom = 3

        self.player = player.Player(math.Vector2(0, 0), self)
        self.player.zIndex = 3
        self.mapGrid = [[None for _ in range(self.map.width)] for _ in range(self.map.height)]
        self.mapTiles = []
        self.zones = []

        for layer in self.map:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, image in layer.tiles():
                    if layer.name != "0":
                        obj = renderer.imageObject(math.Vector2(x * 16, y * 16), image, self)
                        obj.layer = layer.name
                        #obj.obj.w = 16
                        #obj.obj.h = 16
                        obj.zIndex = int(layer.name)
                        self.mapGrid[x][y] = obj
                        self.mapTiles.append(obj)
                        obj.updateImage()
                        obj.debug = True
            elif isinstance(layer, pytmx.TiledObjectGroup):
                if layer.name != "zones":
                    for obj in self.map.get_layer_by_name(layer.name):
                        if obj != None:
                            if obj.image != None:
                                objI = renderer.imageObject(math.Vector2(obj.x, obj.y), obj.image, self)
                                objI.layer = layer.name
                                objI.data = obj
                                objI.zIndex = int(layer.name)
                                objI.updateImage()
                                handleObjects(objI)
        for obj in self.map.get_layer_by_name("zones"):
                    self.zones.append(zoneManager.zone(obj))

    
        self.player.setPos(spawns[0].obj.x, spawns[0].obj.y)
    def update(self, dt):
        self.camera.position = self.camera.position.lerp(math.Vector2(self.player.obj.x, self.player.obj.y), 0.1)
        self.player.update(dt)
        