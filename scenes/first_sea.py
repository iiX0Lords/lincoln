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
    
def rot_center(image, angle, x, y):
    rotated_image = py.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(center = image.get_rect(center = (x, y)).center)
    return rotated_image, new_rect

#TODO add save file
class first_sea(renderer.scene):
    def __init__(self):
        renderer.scene.__init__(self)
        self.active = True

        self.map = tiledPygame.load_pygame("assets/maps/first_sea.tmx")

        self.camera.zoom = 3

        self.player = player.Player(vector2.Vector2(0, 0), self)
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
                        if obj != None:
                            if obj.image != None:
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
        

        for zone in self.zones:
            x, y = zone.obj.x, zone.obj.y
            w, h = zone.obj.width, zone.obj.height

            if self.player.obj.x > x and self.player.obj.x < x + w and self.player.obj.y > y and self.player.obj.y < y + h:
                zone.active = True
                self.player.currentZone = zone
            else:
                zone.active = False
                self.player.currentZone = None


        direction = vector2.Vector2(py.mouse.get_pos()[0], py.mouse.get_pos()[1]).toWorldSpace(self.camera, py.display.get_surface()) - vector2.Vector2(self.player.obj.x, self.player.obj.y)
        radius, angle = direction.as_polar()
        targetAngle = -angle
        rotationSpeed = 7
        angleDiff = (targetAngle - self.player.angle) % 360
        if angleDiff > 180:
            angleDiff -= 360
        elif angleDiff < -180:
            angleDiff += 360

        deadzone = 5
        if abs(angleDiff) < deadzone:
            angleDiff = 0

        rotationVelocity = angleDiff * rotationSpeed
        rotationVelocity = max(-rotationSpeed, min(rotationVelocity, rotationSpeed))
        self.player.angle += rotationVelocity
        self.player.angle = self.player.angle % 360

        rotatedImage, newRect = rot_center(self.player.image, self.player.angle, self.player.obj.w/2, self.player.obj.h/2)
        new_x = self.player.obj.x + (newRect.centerx - self.player.obj.w/2)
        new_y = self.player.obj.y + (newRect.centery - self.player.obj.h/2)
        self.player.obj.x = new_x
        self.player.obj.y = new_y
        self.player.rotated = rotatedImage
    def events(self, event):
        if event.type == py.MOUSEMOTION:
            pass