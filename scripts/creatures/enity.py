import pygame as py
import scripts.engine.renderer as renderer
import scripts.engine.math as math
import scripts.engine.input as input
import scripts.zones as zoneManager
import pytmx

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
        self.velocity = math.Vector2(0, 0)
        self.currentZone = None
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