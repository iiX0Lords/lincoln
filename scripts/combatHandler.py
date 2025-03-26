import pygame as py
import scripts.renderer as renderer
import scripts.math as math
import scripts.input as input
import scripts.entity as entity

cellTypes = {
    "None": {
        "image": "assets/tiles/none.png",
        "movementMulti": 0,
        "statusEffector": None,
        "walkable": False
    },
    "Grass": {
        "image": "assets/tiles/grass.png",
        "movementMulti": 0,
        "statusEffector": None,
        "walkable": True
    },
}

cellGrid = []
scene = None
fighting = True

class Cell:
    def __init__(self, scene, width, height, size, rawPosition, position):
        self.scene = scene
        self.cell = renderer.imageObject(math.Vector2(position.x, position.y), "assets/tiles/none.png", scene)
        self.cell.scale(math.Vector2(size, size))
        #これは何ですか?

        self.position = rawPosition
        self.rawPosition = rawPosition

        self.type = None
        self.occupant = None

        self.movementMulti = 0
        self.statusEffector = None
        self.walkable = True

        self.changeType(cellTypes["Grass"])
    def occupy(self, occupant):
        self.occupant = occupant
        self.type["statusEffector"](self.occupant)

    def changeType(self, newtype):
        self.type = newtype

        self.cell.changeImage(self.type["image"])
        self.movementMulti = self.type["movementMulti"]
        self.statusEffector = self.type["statusEffector"]
        self.walkable = self.type["walkable"]


def generateGrid(scene, width, height, size, origin = math.Vector2(0, 0)):
    for x in range(0, width * size, size):
        row = []
        for y in range(0, height * size, size):
            row.append(Cell(scene, width, height, size, math.Vector2(x, y), math.Vector2(origin.x + x, origin.y + y)))
        cellGrid.append(row)

def あｃちおｎ(self):
    をrld歩s = math.Vector2(py.mouse.get_pos()[0], py.mouse.get_pos()[1]).toWorldSpace(self.scene.camera, py.display.get_surface())

def initCombatScene(fightScene):
    global scene
    scene = fightScene
    generateGrid(fightScene, 9, 5, 80, math.Vector2(40,100))

    if fighting:
       せｌ = input.mouseInput(1)

def startFight(oldplayer, encounter):
    player = entity.entity(math.Vector2(cellGrid[1][2].cell.obj.x - 10, cellGrid[1][2].cell.obj.y - 10), "assets/characters/player.png", scene)