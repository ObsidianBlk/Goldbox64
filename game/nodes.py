
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
            "environment":"",
            "walls":""
        }
        self._topdown = {
            "size":8, # Pixels square
            "wall_color":pygame.Color(255, 255, 255),
            "blocked_color":pygame.Color(255, 0, 0)
        }
        self._orientation = "n"

    @property
    def environment_resource(self):
        return self._res["horizon"]

    @property
    def wall_resource(self):
        return self._res["walls"]

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


    def set_resources(self, environment, walls):
        res = self.resource
        if environment != self._res["environment"]:
            if res.is_valid("graphic", environment):
                self._res["environment"] = environment
        if walls != self._res["walls"]:
            if res.is_valid("graphic", walls):
                self._res["walls"] = walls


    def add_layer(self, name, w, h):
        if name == "" or name in self._layers:
            return
        self._layer[name] = {
            "w":w,
            "h":h,
            "cells":[]
        }
        for c in range(0, w*h):
            self._layer[name]["cells"][c] = {
                "c":0, # Sky / Ceiling
                "g":0, # Ground
                "n":[-1,False], # North Wall | [<graphic index, -1 = None>, <blocking>]
                "s":[-1,False], # South Wall
                "e":[-1,False], # East Wall
                "w":[-1,False] # West Wall
            }
        if self._currentLayer == "":
            self._currentLayer = name

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
        pos = self.position
        lsize = (self.current_layer_width, self.current_layer_height)
        hcells = int(size[0] / cell_size)
        vcells = int(size[1] / cell_size)
        cx = pos[0] - int(hcells * 0.5)
        cy = pos[1] - int(vcells * 0.5)
        ry = -4
        for j in range(0, vcells+1):
            y = cy + j
            if y >= 0 and y < lsize[1]:
                rx = -1
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
                            self.draw_lines([(rx+1, ry+1), (rx+(cell_size-1), ry+1)], self._topdown["blocked_color"], 1)
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



class MapEditor(gbe.nodes.Node2D):
    def __init__(self, name="MapEditor", parent=None):
        try:
            gbe.nodes.Node2D.__init__(self, name, parent)
        except gbe.nodes.Node2D as e:
            raise e

    def on_start(self):
        pass

    def on_pause(self):
        pass








