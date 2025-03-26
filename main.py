import pygame as py
import scripts.renderer as renderer
import scripts.math as math
import scripts.input as input
import scripts.combatHandler as combat
import scripts.entity as entity

py.init()
py.display.set_caption('Lincoln')

window = py.display.set_mode((800, 600))
clock = py.time.Clock()

running = True
dt = 0

mainScene = renderer.scene()
fightScene = renderer.scene()
#bg = renderer.imageObject(math.Vector2(), "assets/backgrounds/sky_day.png", fightScene)
#bg.scale(math.Vector2(1024 * 3, 512 * 3))

combat.initCombatScene(fightScene)

player = entity.entity(math.Vector2(0, 0), "assets/tiles/none.png", mainScene)


def change(*self):
    #global fighting
    #fighting = not fighting
    combat.startFight(player, [])

escape = input.keyInput(py.K_ESCAPE)
escape.onDown = change

while running:

    window.fill("black")

    for event in py.event.get():
        if event.type == py.QUIT:
            running = False
        input.handleInput(event)

    mainScene.camera.position.x += 1

    if combat.fighting:
        fightScene.render(window)
    else:
        mainScene.render(window)

    py.display.flip()

    dt = clock.tick(60) / 1000