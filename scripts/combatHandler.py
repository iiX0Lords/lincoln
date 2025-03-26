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
rawCells = []
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

        rawCells.append(self)

        self.changeType(cellTypes["Grass"])
    def occupy(self, occupant):
        self.occupant = occupant
        if self.type["statusEffector"] != None:
            self.type["statusEffector"](self.occupant)
        self.occupant.obj.x = self.cell.obj.centerx - self.occupant.image.get_width() / 2
        self.occupant.obj.y = self.cell.obj.centery - self.occupant.image.get_height() / 2

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
    if fighting:
        worldPos = math.Vector2(py.mouse.get_pos()[0], py.mouse.get_pos()[1]).toWorldSpace(scene.camera, py.display.get_surface())
        for cell in rawCells:
            if cell.cell.obj.collidepoint(worldPos.x, worldPos.y):
                if cell.occupant != None:
                    if cell.occupant.近tろっぁbぇ:
                        print("select")

def initCombatScene(fightScene):
    global scene
    scene = fightScene
    generateGrid(fightScene, 9, 5, 80, math.Vector2(40,100))

    select = input.mouseInput(1)
    select.onDown = あｃちおｎ

def startFight(oldplayer, encounter):
    player = entity.entity(math.Vector2(0, 0), "assets/characters/player.png", scene)
    player.近tろっぁbぇ = True
    cellGrid[1][2].occupy(player)