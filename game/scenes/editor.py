
from .. import gbe
from ..nodes import *

_TREE = None
def get():
    global _TREE
    if _TREE is None:
        root = gbe.nodes.NodeSurface("Editor")
        root.scale_to_display = True
        root.keep_aspect_ratio = True
        root.align_center = True
        root.set_surface((64, 64))
        root.set_clear_color((0,0,0,0))

        gamemap = NodeGameMap("GameMap", root)
        gamemap.set_resources("", "walls.json")
        gamemap.add_layer("main", 10, 10)

        editor = NodeMapEditor("Editor", gamemap)

        _TREE = root
    return _TREE
