import pygame as py

class Vector2(py.Vector2):
    def toWorldSpace(self, camera, screen):
        screen_width, screen_height = screen.get_width(), screen.get_height()
        scale_x, scale_y = camera.zoom, camera.zoom
        camera_x, camera_y = camera.position.x, camera.position.y
        normalized_x = (self.x - screen_width / 2) / scale_x
        normalized_y = (self.y - screen_height / 2) / scale_y

        world_x = normalized_x + camera_x
        world_y = normalized_y + camera_y
        
        return Vector2(world_x, world_y)
    
    def toScreenSpace(self, camera, screen):
        screen_width, screen_height = screen.get_width(), screen.get_height()
        scale_x, scale_y = camera.zoom, camera.zoom
        camera_x, camera_y = camera.position.x, camera.position.y
        screen_x = (self.x - camera_x) * scale_x + screen_width / 2
        screen_y = (self.y - camera_y) * scale_y + screen_height / 2
        
        return Vector2(screen_x, screen_y)