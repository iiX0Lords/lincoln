from __future__ import division
import pygame as py
import scripts.engine.renderer as renderer
import scripts.engine.math as math
import scripts.engine.input as input
import sys
sys.dont_write_bytecode = True

py.init()
py.display.set_caption('Lincoln')

window = py.display.set_mode((800, 600))
clock = py.time.Clock()

running = True
dt = 0

import scenes.first_sea
firstSea = scenes.first_sea.first_sea()

while running:

    window.fill(py.Color(25, 83, 191))

    for event in py.event.get():
        if event.type == py.QUIT:
            running = False
        input.handleInput(event)
        for scene in renderer.scenes:
            if scene.active == True:
                scene.events(event)

    for scene in renderer.scenes:
        if scene.active == True:
            scene.update(dt)
            scene.render(window)

    py.display.flip()

    #print(clock.get_fps())
    dt = clock.tick(60) / 1000