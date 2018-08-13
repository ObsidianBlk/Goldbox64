
from . import gbe
import pygame

class NodeInterface(gbe.nodes.NodeSurface):
    def __init__(self, name="Interface", parent=None):
        try:
            gbe.nodes.NodeSurface.__init__(self, name, parent)
        except gbe.nodes.NodeError as e:
            raise e

    def on_render(self):
        size = self.resolution
        self.draw_rect((0, 0, size[0], 10), pygame.Color(255,0,0,128), 1)
        self.draw_circle((int(size[0]/2), int(size[1]/2)), 16, pygame.Color(255,0,0,255), 2, pygame.Color(0,255,0,255))



class NodeGameMap(gbe.nodes.Node2D):
    def __init__(self, name="GameMap", parent=None):
        try:
            gbe.nodes.Node2D.__init__(self, name, parent)
        except gbe.nodes.NodeError as e:
            raise e
        self._renderMode = 0 # 0 = Top-down | 1 = Perspective
        self._layer = {}
        self._currentLayer = ""
        self._res = {
            "env_src":"",
            "env":None,
            "wall_src":"",
            "walls":None,
            "wall_index":-1,
            "door_index":-1
        }
        self._topdown = {
            "size":8, # Pixels square
            "wall_color":pygame.Color(255, 255, 255),
            "blocked_color":pygame.Color(255, 0, 0)
        }
        self._cellpos = [0,0]
        self._orientation = "n"

    @property
    def environment_source(self):
        return self._res["env_src"]

    @property
    def wall_source(self):
        return self._res["wall_src"]

    @property
    def layer_count(self):
        return len(self._layer)

    @property
    def current_layer(self):
        return self._currentLayer

    @property
    def current_layer_width(self):
        if self._currentLayer != "":
            return self._layer[self._currentLayer]["w"]
        return 0

    @property
    def current_layer_height(self):
        if self._currentLayer != "":
            return self._layer[self._currentLayer]["h"]
        return 0

    @property
    def layer_names(self):
        names = []
        for key in self._layer:
            names.append(names)
        return names

    @property
    def orientation(self):
        return self._orientation

    @property
    def cell_position(self):
        return (self._cellpos[0], self._cellpos[1])

    def set_resources(self, env_src, wall_src):
        res = self.resource
        if env_src != "" and env_src != self._res["env_src"]:
            if res.is_valid("json", env_src):
                if not res.has("json", env_src):
                    res.store("json", env_src)
                e = res.get("json", env_src)
                if e is not None and e() is not None:
                    self._res["env_src"] = env_src
                    self._res["env"] = e
                    # TODO: Load the images associated with the environments
        if wall_src != "" and wall_src != self._res["wall_src"]:
            if res.is_valid("json", wall_src):
                if not res.has("json", wall_src):
                    print("Storing resource {}".format(wall_src))
                    res.store("json", wall_src)
                w = res.get("json", wall_src)
                print(w)
                if w is not None and w() is not None:
                    self._res["wall_src"] = wall_src
                    self._res["walls"] = w
                    # NOTE: I'm making a lot of assumptions to the structural validity of the data file, but...
                    imgsrc = w().data["src"]
                    if res.is_valid("graphic", imgsrc):
                        if res.has("graphic", imgsrc):
                            res.store("graphic", imgsrc)
                else:
                    print("Failed to get JSON instance {}".format(wall_src))
            else:
                print("Invalid JSON {}".format(wall_src))


    def add_layer(self, name, w, h):
        if name == "" or name in self._layer:
            return
        self._layer[name] = {
            "w":w,
            "h":h,
            "cells":[]
        }
        for c in range(0, w*h):
            self._layer[name]["cells"].append({
                "c":0, # Sky / Ceiling
                "g":0, # Ground
                "n":[-1, False, -1, None], # North Wall | [<graphic index, -1 = None>, <blocking>, <door index, -1 = None, 0 = closed, 1=open>, <door target>]
                "s":[-1, False, -1, None], # South Wall
                "e":[-1, False, -1, None], # East Wall
                "w":[-1, False, -1, None], # West Wall
            })
        if self._currentLayer == "":
            self._currentLayer = name

    def set_active_layer(self, name, x=0, y=0):
        if name == "" or not (name in self._layers):
            return
        layer = self._layers[name]
        if x >= 0 and x < layer["w"] and y >= 0 and y < layer["h"]:
            self._currentLayer = name
            self._cellpos = [x,y]

    def set_cell_env(self, x, y, ceiling=-1, ground=-1):
        if self._currentLayer == "":
            return
        layer = self._layer[self._currentLayer]
        if x >= 0 and x < layer["w"] and y >= 0 and y < layer["h"]:
            index = (y * layer["w"]) + x
            cell = layer["cells"]
            if ceiling >= 0:
                cell[index]["c"] = ceiling
            if ground >= 0:
                cell[index]["g"] = ground

    def fill_cell_env(self, x1, y1, x2, y2, ceiling=-1, ground=-1):
        if self._currentLayer == "":
            return
        for y in range(y1, y2+1):
            for x in range(x1, x2+1):
                self.set_cell_env(x, y, ceiling, ground)

    def set_cell_face(self, x, y, face, gi=-2, blocking=None):
        if self._currentLayer == "" or not (face == "n" or face == "s" or face == "w" or face == "e"):
            return
        layer = self._layer[self._currentLayer]
        if x >= 0 and x < layer["w"] and y >= 0 and y < layer["h"]:
            index = (y * layer["w"]) + x
            cell = layer["cells"]
            if gi <= -2:
                gi = self._res["wall_index"]
            if gi >= -1:
                cell[index][face][0] = gi
                if blocking is not None:
                    cell[index][face][1] = (blocking == True)
                else:
                    if gi == -1: # If gi = -1, there is no wall, so, by default, there is no blocking.
                        cell[index][face][1] = False
                    else: # Otherwise, blocking is assumed :)
                        cell[index][face][1] = True
            elif blocking is not None:
                blocking = (blocking == True) # Forcing a boolean
                cell[index][face][1] = blocking  

    def next_wall(self):
        if self._res["walls"] is not None:
            w = self._res["walls"]()
            if w is not None:
                windex = self._res["wall_index"] + 1
                if windex >= len(w.data["walls"]):
                    windex = -1
                self._res["wall_index"] = windex
                print("Next Wall Index: {}".format(windex))

    def prev_wall(self):
        if self._res["walls"] is not None:
            w = self._res["walls"]()
            if w is not None:
                windex = self._res["wall_index"] - 1
                if windex < -1:
                    windex = len(w.data["walls"]) - 1
                self._res["wall_index"] = windex
                print("Prev Wall Index: {}".format(windex))

    def turn_left(self):
        onum = self._d_s2n(self._orientation)
        onum -= 1
        if onum < 0:
            onum = 3
        self._orientation = self._d_n2s(onum)

    def turn_right(self):
        onum = self._d_s2n(self._orientation)
        onum += 1
        if onum > 3:
            onum = 0
        self._orientation = self._d_n2s(onum)

    def move_to(self, x, y):
        if x >= 0 and x < self.current_layer_width and y >= 0 and y < self.current_layer_height:
            self._cellpos = [x, y]

    def move_forward(self, ignore_passible=False):
        if ignore_passible or self.is_passible(self._cellpos[0], self._cellpos[1], self._orientation):
            x = self._cellpos[0]
            y = self._cellpos[1]
            if self._orientation == "n":
                y -= 1
            elif self._orientation == "e":
                x += 1
            elif self._orientation == "s":
                y += 1
            elif self._orientation == "w":
                x -= 1
            self.move_to(x, y)

    def move_backward(self, ignore_passible=False):
        orient = self._orientation
        if self._orientation == "n":
            self._orientation = "s"
        elif self._orientation == "s":
            self._orientation = "n"
        elif self._orientation == "e":
            self._orientation = "w"
        elif self._orientation == "w":
            self._orientation = "e"
        self.move_forward(ignore_passible)
        self._orientation = orient

    def is_passible(self, x, y, d):
        """
        Returns true if it's possible to move forward from the x, y map position in the direction given.
        d - 0 = North, 1 = East, 2 = South, 3 = West
        """
        if self._currentLayer == "" or d < 0 or d >= 4:
            return False
        layer = self._layer[self._currentLayer]
        if x >= 0 and x < layer["w"] and y >= 0 and y < layer["h"]:
            index = (y * layer["w"]) + x
            d = self._d_n2s(d)
            return not layer["cells"][index][d][1]
        return False


    def _d_n2s(self, d): # _(d)irection_(n)umber_to_(s)tring
        if d == 0:
            return "n"
        elif d == 1:
            return "e"
        elif d == 2:
            return "s"
        elif d == 3:
            return "w"
        return ""

    def _d_s2n(self, d):
        if d == "n":
            return 0
        elif d == "e":
            return 1
        elif d == "s":
            return 2
        elif d == "w":
            return 3
        return -1

    def _indexFromPos(self, x, y):
        if x >= 0 and x < self.current_layer_width and y >= 0 and y < self.current_layer_height:
            return (y * self.current_layer_width) + x
        return -1

    def _getCell(self, x, y):
        index = self._indexFromPos(x, y)
        if index < 0:
            return None
        return self._layer[self._currentLayer]["cells"][index]


    def _RenderTopDown(self):
        cell_size = self._topdown["size"]
        size = self.resolution
        pos = self._cellpos
        lsize = (self.current_layer_width, self.current_layer_height)
        hcells = int(size[0] / cell_size)
        vcells = int(size[1] / cell_size)
        cx = pos[0] - int(hcells * 0.5)
        cy = pos[1] - int(vcells * 0.5)
        ry = -int(cell_size*0.5)
        for j in range(0, vcells+1):
            y = cy + j
            if y >= 0 and y < lsize[1]:
                rx = -int(cell_size*0.5)
                for i in range(0, hcells+1):
                    x = cx + i
                    if x >= 0 and x < lsize[0]:
                        cell = self._getCell(x, y)
                        if cell["n"][0] >= 0:
                            self.draw_rect((rx, ry, cell_size, 2), self._topdown["wall_color"], 0, self._topdown["wall_color"])
                        if cell["e"][0] >= 0:
                            self.draw_rect((rx+(cell_size-2), ry, 2, cell_size), self._topdown["wall_color"], 0, self._topdown["wall_color"])
                        if cell["s"][0] >= 0:
                            self.draw_rect((rx, ry+(cell_size-2), cell_size, 2), self._topdown["wall_color"], 0, self._topdown["wall_color"])
                        if cell["w"][0] >= 0:
                            self.draw_rect((rx, ry, 2, cell_size), self._topdown["wall_color"], 0, self._topdown["wall_color"])

                        if cell["n"][1] == True:
                            self.draw_lines([(rx+1, ry+1), (rx+(cell_size-2), ry+1)], self._topdown["blocked_color"], 1)
                        if cell["e"][1] == True:
                            self.draw_lines([(rx+(cell_size-2), ry+1), (rx+(cell_size-2), ry+(cell_size-2))], self._topdown["blocked_color"], 1)
                        if cell["s"][1] == True:
                            self.draw_lines([(rx+1, ry+(cell_size-2)), (rx+(cell_size-2), ry+(cell_size-2))], self._topdown["blocked_color"], 1)
                        if cell["w"][1] == True:
                            self.draw_lines([(rx+1, ry+1), (rx+1, ry+(cell_size-2))], self._topdown["blocked_color"], 1)
                    rx += cell_size    
            ry += cell_size



    def _RenderPerspective(self):
        pass

    def on_render(self):
        if self._renderMode == 0:
            self._RenderTopDown()
        else:
            self._RenderPerspective()



class NodeMapEditor(gbe.nodes.Node2D):
    def __init__(self, name="MapEditor", parent=None):
        try:
            gbe.nodes.Node2D.__init__(self, name, parent)
        except gbe.nodes.Node2D as e:
            raise e
        self._last_orientation = ""
        self._size = 0
        self._thickness = 1
        self._color = pygame.Color(255,255,255)
        self._points = None
        self.pointer_size = 4

    def _getPoints(self, size):
        p = self.parent
        o = p.orientation
        points = self._points[o]

        hw = int(size[0]*0.5)
        hh = int(size[1]*0.5)
        return (
            (points[0][0] + hw, points[0][1] + hh),
            (points[1][0] + hw, points[1][1] + hh),
            (points[2][0] + hw, points[2][1] + hh)
        )

    @property
    def pointer_size(self):
        return self._size
    @pointer_size.setter
    def pointer_size(self, size):
        if not isinstance(size, int):
            raise TypeError("Size expected to be an integer.")
        if size <= 0:
            raise ValueError("Size must be greater than zero.")
        if size != self._size:
            self._size = size

            # Now updating all of the pointer... ummm... points
            hs = max(1, int(size * 0.5))
            self._points = {
                "n": ((0,-hs),(hs,hs),(-hs,hs)),
                "s": ((0,hs),(hs,-hs),(-hs,-hs)),
                "e": ((-hs,hs),(hs,0),(-hs,-hs)),
                "w": ((hs,hs),(-hs,0),(hs,-hs))
            }

    def on_start(self):
        self.listen("KEYPRESSED", self.on_keypressed)

    def on_pause(self):
        self.unlisten("KEYPRESSED", self.on_keypressed)

    def on_keypressed(self, event, data):
        p = self.parent
        if p is None or not isinstance(p, NodeGameMap):
            return

        if data["key_name"] == "escape":
            self.emit("QUIT")
        if data["key_name"] == "w":
            p.move_forward(True)
        elif data["key_name"] == "s":
            p.move_backward(True)
        elif data["key_name"] == "a":
            p.turn_left()
        elif data["key_name"] == "d":
            p.turn_right()
        elif data["key_name"] == "space":
            o = p.orientation
            cpos = p.cell_position
            p.set_cell_face(cpos[0], cpos[1], o)
        elif data["key_name"] == "e":
            p.next_wall()
        elif data["key_name"] == "q":
            p.prev_wall()

    def on_render(self):
        size = self.resolution
        self.draw_lines(self._getPoints(size), self._color, self._thickness, True)





