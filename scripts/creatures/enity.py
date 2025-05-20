import pygame as py
import scripts.engine.renderer as renderer
import scripts.engine.math as math
import scripts.engine.input as input
import scripts.ui.backpack as backpack
import scripts.magic.magics as magics
import pytmx

class Entity(renderer.imageObject):
    def __init__(self, position, image, scene):
        renderer.imageObject.__init__(self, position, image, scene)
        self.stats = {
            "mp": 0,
            "str": 0,
        }
        self.humanoid = {
            "health": 100,
            "maxHealth": 100,
            "energy": 30,
            "maxEnergy" : 30,
            "speed": 1
        }
        self.ai = False
        self.velocity = math.Vector2(0, 0)
        self.currentZone = None
        self.standingTile = None
        self.backpack = backpack.backpack(scene)
        self.magic = None

        self.angle = 0

    def addMagic(self, magic):
        magicClass = getattr(magics, magic, None)
        if magicClass:
            self.magic = magicClass(self)
            self.backpack.addTool(self.magic, 0)

    def stateChange(self, state):
        pass

    def takeDamage(self, amount):
        self.stats["health"] -= amount
    def heal(self, amount):
        self.stats["health"] += amount
    def get_tile(self, tmxdata, local):
        world_x = local.toWorldSpace(self.scene.camera, py.display.get_surface()).x
        world_y = local.toWorldSpace(self.scene.camera, py.display.get_surface()).y
        tile_x = int(world_x // 16)
        tile_y = int(world_y // 16)

        for layer in reversed(list(tmxdata.visible_layers)):
            if isinstance(layer, pytmx.TiledTileLayer):
                gid = layer.data[tile_x][tile_y]
                if gid:
                    tile_props = tmxdata.get_tile_properties_by_gid(gid)
                    return {
                        "layer": layer.name,
                        "gid": gid,
                        "tile_x": tile_x,
                        "tile_y": tile_y,
                        "properties": tile_props
                    }

        return None
    def collide(self, previousPosition):
        self.obj.x = previousPosition.x; self.obj.y = previousPosition.y
    def pointAt(self, position, rotationSpeed, deadzone = 5):
        direction = position.toWorldSpace(self.scene.camera, py.display.get_surface()) - math.Vector2(self.obj.x, self.obj.y)
        radius, angle = direction.as_polar()
        targetAngle = -angle
        angleDiff = (targetAngle - self.angle) % 360
        if angleDiff > 180:
            angleDiff -= 360
        elif angleDiff < -180:
            angleDiff += 360
        
        if abs(angleDiff) < deadzone:
            angleDiff = 0

        rotationVelocity = angleDiff * rotationSpeed
        rotationVelocity = max(-rotationSpeed, min(rotationVelocity, rotationSpeed))
        self.angle += rotationVelocity
        self.angle = self.angle % 360

        rotatedImage, newRect = self.rot_center(self.image, self.angle, self.obj.w/2, self.obj.h/2)
        new_x = self.obj.x + (newRect.centerx - self.obj.w/2)
        new_y = self.obj.y + (newRect.centery - self.obj.h/2)
        self.obj.x = new_x
        self.obj.y = new_y
        self.rotated = rotatedImage
    def collisionCheck(self, previousPosition):
        localselfPosition = math.Vector2(self.obj.x, self.obj.y).toScreenSpace(self.scene.camera, py.display.get_surface())
        localselfPositionCenter = math.Vector2(self.obj.x + 8, self.obj.y + 8).toScreenSpace(self.scene.camera, py.display.get_surface())
        localSelfRect = py.Rect(localselfPosition.x, localselfPosition.y, self.obj.w, self.obj.h)

        if self.currentZone is not None:
            for tile in self.currentZone.mapTiles:
                tile.debugColour = py.Color(0, 255, 0)

                localtilePosition = math.Vector2(tile.obj.x, tile.obj.y).toScreenSpace(self.scene.camera, py.display.get_surface())
                localTileRect = py.Rect(localtilePosition.x, localtilePosition.y, tile.obj.w, tile.obj.h)

                if localSelfRect.colliderect(localTileRect):
                    tile.debugColour = py.Color(255, 0, 0)
                    if tile.zIndex == 3:
                        self.collide(previousPosition)

            tile = self.get_tile(self.scene.map, localselfPositionCenter)
            tile = self.currentZone.mapGrid[tile["tile_x"]][tile["tile_y"]]
            if tile:
                tile.debugColour = py.Color(0, 0, 255)
                self.standingTile = tile