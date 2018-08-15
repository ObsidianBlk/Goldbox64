
from .. import gbe
from ..nodes import *

_TREE = None
def get():
    global _TREE
    if _TREE is None:
        root = gbe.nodes.NodeSurface("MAIN_MENU")
        root.scale_to_display = True
        root.keep_aspect_ratio = True
        root.align_center = True
        root.set_surface((64, 64))
        root.set_clear_color((0,0,0,0))

        gmap = NodeGameMap("gm", root)
        gmap.set_resources("environment.json", "walls.json")
        gmap.set_render_mode(1)
        gmap.load_map("main", False)

        mwalker = NodeMapWalker("MapWalker", gmap)

        menu = NodeOptions("Options", root)
        #menu.add_option("IttyBitty.ttf", 4, "Game", "SCENECHANGE", {"scene":"Game", "hold":False})
        menu.add_option("IttyBitty.ttf", 4, "Editor", "SCENECHANGE", {"scene":"Editor", "hold":False})
        menu.add_option("IttyBitty.ttf", 4, "Quit", "QUIT")
        menu.position = (10, 14)

        overlay = gbe.nodes.NodeSprite("Overlay", root)
        overlay.image = "MainMenu_Logo.png"
        _TREE = root
    return _TREE
