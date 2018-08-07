'''
    Filename nodes.py
    Author: Bryan "ObsidianBlk" Miller
    Date Created: 8/1/2018
    Python Version: 3.7
'''

from .display import Display
from .events import Events
from .resource import ResourceManager
import pygame


class NodeError(Exception):
    pass


class Node:
    def __init__(self, name="Node", parent=None):
        self._NODE_DATA={
            "parent":None,
            "name":name,
            "children":[],
            "resource":None
        }
        if parent is not None:
            try:
                self.parent = parent
            except NodeError as e:
                raise e

    @property
    def parent(self):
        return self._NODE_DATA["parent"]

    @parent.setter
    def parent(self, new_parent):
        try:
            self.parent_to_node(new_parent)
        except NodeError as e:
            raise e

    @property
    def root(self):
        if self.parent is None:
            return self
        return self.parent.root

    @property
    def name(self):
        return self._NODE_DATA["name"]

    @name.setter
    def name(self, value):
        if self.parent is not None:
            if self.parent.get_node(value) is not None:
                raise NodeError("Parent already contains node named '{}'.".format(name))
        self._NODE_DATA["name"] = value

    @property
    def full_name(self):
        if self.parent is None:
            return self.name
        return self.parent.full_name + "." + self.name

    @property
    def resource(self):
        if self._NODE_DATA["resource"] is None:
            # Only bother creating the instance if it's being asked for.
            # All ResourceManager instances access same data.
            self._NODE_DATA["resource"] = ResourceManager()
        return self._NODE_DATA["resource"]

    @property
    def child_count(self):
        return len(this._NODE_DATA["children"])

    def get_world_position(self):
        if self.parent is None:
            return (0,0)
        return self.parent.get_world_position()

    def parent_to_node(self, parent, allow_reparenting=False):
        if not isinstance(value, Node):
            raise NodeError("Node may only parent to another Node instance.")
        if self.parent is None or self.parent != parent:
            if self.parent is not None:
                if allow_Reparenting == False:
                    raise NodeError("Node already assigned a parent Node.")
                if self.parent.remove_node(self) != self:
                    raise NodeError("Failed to remove self from current parent.")
            try:
                parent.attach_node(self)
            except NodeError as e:
                raise e


    def attach_node(self, node, reparent=False, index=-1):
        if node.parent is not None:
            if node.parent == self:
                return # Nothing to do. Given node already parented to this node.
            if reparent == False:
                raise NodeError("Node already parented.")
            if node.parent.remove_node(node) != node:
                raise NodeError("Failed to remove given node from it's current parent.")
        if self.get_node(node.name) is not None:
            raise NodeError("Node with name '{}' already attached.".format(node.name))
        node._NODE_DATA["parent"] = self
        children = self._NODE_DATA["children"]
        if index < 0 or index >= len(children):
            children.append(node)
        else:
            children.insert(index, node)

    def remove_node(self, node):
        if isinstance(node, (str, unicode)):
            n = self.get_node(node)
            if n is not None:
                try:
                    return self.remove_node(n)
                except NodeError as e:
                    raise e
        elif isinstance(node, Node):
            if node.parent != self:
                if node.parent == None:
                    raise NodeError("Cannot remove an unparented node.")
                try:
                    return node.parent.remove_node(node)
                except NodeError as e:
                    raise e
            if node in self._NODE_DATA["children"]:
                self._NODE_DATA["children"].remove(node)
                node._NODE_DATA["parent"] = None
                return node
        else:
            raise NodeError("Expected a Node instance or a string.")
        return None


    def get_node(self, name):
        if self.child_count <= 0:
            return None

        subnames = name.split(".")
        for c in self._NODE_DATA["children"]:
            if c.name == subnames[0]:
                if len(subnames) > 1:
                    return c.get_node(".".join(subnames[1:-1]))
                return c
        return None


    def _update(self, dt):
        if hasattr(self, "on_update"):
            self.on_update(dt)

        for c in self._NODE_DATA["children"]:
            c._update(dt)

    def _render(self, surface):
        for c in self._NODE_DATA["children"]:
            c._render(surface)




class Node2D(Node):
    def __init__(self, name="Node2D", parent=None):
        try:
            Node.__init__(self, name, parent)
        except NodeError as e:
            raise e
        self._NODE2D_DATA={
            "position":[0.0, 0.0]
        }

    @property
    def position(self):
        p = self._NODE2D_DATA["position"]
        return (p[0], p[1])
    @position.setter
    def position(self, pos):
        if not isinstance(pos, (list, tuple)):
            raise TypeError("Expected a list or tuple.")
        if len(pos) != 2:
            raise ValueError("Wrong number of values given.")
        try:
            self.position_x = pos[0]
            self.position_y = pos[1]
        except Exception as e:
            raise e

    @property
    def position_x(self):
        return self._NODE2D_DATA["position"][0]
    @position_x.setter
    def position_x(self, v):
        if not isinstance(v, (int, float)):
            raise TypeError("Excepted an number value.")
        self._NODE2D_DATA["position"][0] = float(v)

    @property
    def position_y(self):
        return self._NODE2D_DATA["position"][1]
    @position_y.setter
    def position_y(self, v):
        if not isinstance(v, (int, float)):
            raise TypeError("Excepted an number value.")
        self._NODE2D_DATA["position"][1] = float(v)

    def _callOnRender(self, surface):
        if hasattr(self, "on_render"):
            self._ACTIVE_SURF = surface
            self.on_render()
            del self._ACTIVE_SURF

    def get_world_position(self):
        pos = self.position
        if self.parent is None:
            return pos
        ppos = self.parent.get_world_position()
        return (pos[0] + ppos[0], pos[1] + ppos[1])

    def _render(self, surface):
        self._callOnRender(surface)
        Node._render(self, surface)

    def draw_image(self, img, pos=(0,0), rect=None):
        if not hasattr(self, "_ACTIVE_SURF"):
            return
        self._ACTIVE_SURF.blit(img, pos, rect)

    def fill(self, color):
        if not hasattr(self, "_ACTIVE_SURF"):
            return
        self._ACTIVE_SURF.fill(color)

    def draw_lines(self, points, color, thickness=1, closed=False):
        if not hasattr(self, "_ACTIVE_SURF"):
            return
        pygame.draw.lines(self._ACTIVE_SURF, color, closed, points, thickness)

    def draw_rect(self, rect, color, thickness=1):
        if not hasattr(self, "_ACTIVE_SURF"):
            return
        pygame.draw.rect(self._ACTIVE_SURF, color, rect, thickness)

    def draw_ellipse(self, rect, color, thickness=1, fill_color=None):
        if not hasattr(self, "_ACTIVE_SURF"):
            return
        if fill_color is not None:
            pygame.draw.ellipse(self._ACTIVE_SURF, fill_color, rect)
        if thickness > 0:
            pygame.draw.ellipse(self._ACTIVE_SURF, color, rect, thickness)

    def draw_circle(self, pos, radius, color, thickness=1, fill_color=None):
        if not hasattr(self, "_ACTIVE_SURF"):
            return
        if fill_color is not None:
            pygame.draw.circle(self._ACTIVE_SURF, fill_color, pos, radius)
        if thickness > 0:
            pygame.draw.circle(self._ACTIVE_SURF, color, pos, radius, thickness)

    def draw_polygon(self, points, color, thickness=1, fill_color=None):
        if not hasattr(self, "_ACTIVE_SURF"):
            return
        if fill_color is not None:
            pygame.draw.polygon(self._ACTIVE_SURF, fill_color, points)
        if thickness >= 1:
            pygame.draw.polygon(self._ACTIVE_SURF, color, points, thickness)




class NodeSurface(Node2D):
    def __init__(self, name="NodeSurface", parent=None):
        try:
            Node2D.__init__(self, name, parent)
        except NodeError as e:
            raise e
        # TODO: Update this class to use the _NODE*_DATA={} structure.
        self._scale = (1.0, 1.0)
        self._scaleToDisplay = False
        self._scaleDirty = False
        self._keepAspectRatio = False
        self._alignCenter = False
        self._surface = None
        self._tsurface = None
        self.set_surface()

    def _updateTransformSurface(self):
        if self._surface is None:
            return

        self._scaleDirty = False
        if self._scaleToDisplay:
            dsize = Display.resolution
            ssize = self._surface.get_size()
            self._scale = (dsize[0] / ssize[0], dsize[1] / ssize[1])
            if self._keepAspectRatio:
                if self._scale[0] < self._scale[1]:
                    self._scale = (self._scale[0], self._scale[0])
                else:
                    self._scale = (self._scale[1], self._scale[1])

        if self._scale[0] == 1.0 and self._scale[1] == 1.0:
            self._tsurface = None
            return
        size = self._surface.get_size()
        nw = size[0] * self._scale[0]
        nh = 0
        if self._keepAspectRatio:
            nh = size[1] * self._scale[0]
        else:
            nh = size[1] * self._scale[1]
        self._tsurface = pygame.Surface((nw, nh), pygame.SRCALPHA, self._surface)
        self._tsurface.fill(pygame.Color(0,0,0,0))

    @property
    def resolution(self):
        if self._surface is None:
            return (0,0)
        return self._surface.get_size()
    @resolution.setter
    def resolution(self, res):
        try:
            self.set_surface(res)
        except (TypeError, ValueError) as e:
            raise e

    @property
    def width(self):
        return self.resolution[0]

    @property
    def height(self):
        return self.resolution[1] 

    @property
    def scale(self):
        return self._scale
    @scale.setter
    def scale(self, scale):
        if self._keepAspectRatio:
            if not isinstance(scale, (int, float)):
                raise TypeError("Expected number value.")
            self._scale = (scale, self._scale[1])
        else:
            if not isinstance(scale, tuple):
                raise TypeError("Expected a tuple")
            if len(scale) != 2:
                raise ValueError("Expected tuple of length two.")
            if not isinstance(scale[0], (int, float)) or not isinstance(scale[1], (int, float)):
                raise TypeError("Expected number values.")
            self._scale = scale
        self._updateTransformSurface()

    @property
    def keep_aspect_ratio(self):
        return self._keepAspectRatio
    @keep_aspect_ratio.setter
    def keep_aspect_ratio(self, keep):
        self._keepAspectRatio = (keep == True)
        self._updateTransformSurface()

    @property
    def align_center(self):
        return self._alignCenter
    @align_center.setter
    def align_center(self, center):
        self._alignCenter = (center == True)

    @property
    def scale_to_display(self):
        return self._scaleToDisplay
    @scale_to_display.setter
    def scale_to_display(self, todisplay):
        if todisplay == True:
            self._scaleToDisplay = True
            Events.listen("VIDEORESIZE", self._OnVideoResize)
        else:
            self._scaleToDisplay = False
            Events.unlisten("VIDEORESIZE", self._OnVideoResize)
        self._updateTransformSurface()

    def scale_to(self, target_resolution):
        if self._surface is not None:
            size = self._surface.get_size()
            nscale = (float(size[0]) / float(target_resolution[0]), float(size[1]) / float(target_resolution[1]))
            self.scale = nscale


    def set_surface(self, resolution=None):
        dsurf = Display.surface
        if resolution is None:
            if dsurf is not None:
                self._surface = dsurf.convert_alpha()
                self._surface.fill(pygame.Color(0,0,0,0))
                self._updateTransformSurface()
        else:
            if not isinstance(resolution, tuple):
                raise TypeError("Expected a tuple.")
            if len(resolution) != 2:
                raise ValueError("Expected a tuple of length two.")
            if not isinstance(resolution[0], int) or not isinstance(resolution[1], int):
                raise TypeError("Tuple expected to contain integers.")
            if dsurf is not None:
                self._surface = pygame.Surface(resolution, pygame.SRCALPHA, dsurf)
            else:
                self._surface = pygame.Surface(resolution, pygame.SRCALPHA)
            self._surface.fill(pygame.Color(0,0,0,0))
            self._updateTransformSurface()

    def _render(self, surface):
        if self._surface is None:
            self.set_surface()
        if self._surface is not None:
            if self._scaleDirty:
                self._updateTransformSurface()
            Node2D._render(self, self._surface)
        else:
            Node2D._render(self, surface)
        self._scale_and_blit(surface)


    def _scale_and_blit(self, dest):
        dsize = dest.get_size()

        src = self._surface
        if self._tsurface is not None:
            pygame.transform.scale(self._surface, self._tsurface.get_size(), self._tsurface)
            src = self._tsurface

        ssize = src.get_size()
        posx = self.position_x
        posy = self.position_y
        if self._alignCenter:
            if dsize[0] > ssize[0]:
                posx += (dsize[0] - ssize[0]) * 0.5
            if dsize[1] > ssize[1]:
                posy += (dsize[1] - ssize[1]) * 0.5
        pos = (int(posx), int(posy))
        dest.blit(src, pos)

    def _OnVideoResize(self, event, data):
        if self._scaleToDisplay:
            self._scaleDirty = True



class NodeSprite(Node2D):
    def __init__(self, name="NodeSprite", parent=None):
        try:
            Node2D.__init__(self, name, parent)
        except NodeError as e:
            raise e
        self._NODESPRITE_DATA={
            "rect":[0,0,0,0],
            "image":"",
            "scale":[1.0, 1.0],
            "surface":None
        }

    @property
    def image_width(self):
        if self._NODESPRITE_DATA["surface"] is None:
            return 0
        surf = self._NODESPRITE_DATA["surface"]()
        return surf.get_width()

    @property
    def image_height(self):
        if self._NODESPRITE_DATA["surface"] is None:
            return 0
        surf = self._NODESPRITE_DATA["surface"]()
        return surf.get_height()

    @property
    def sprite_width(self):
        return int(self.rect_width * self.scale_x)

    @property
    def sprite_height(self):
        return int(self.rect_height * self.scale_y)

    @property
    def rect(self):
        return (self._NODESPRITE_DATA["rect"][0],
            self._NODESPRITE_DATA["rect"][1],
            self._NODESPRITE_DATA["rect"][2],
            self._NODESPRITE_DATA["rect"][3])

    @rect.setter
    def rect(self, rect):
        if not isinstance(rect, (list, tuple)):
            raise TypeError("Expected a list or tuple.")
        if len(rect) != 4:
            raise ValueError("rect value contains wrong number of values.")
        try:
            self.rect_x = rect[0]
            self.rect_y = rect[1]
            self.rect_width = rect[2]
            self.rect_height = rect[3]
        except Exception as e:
            raise e 

    @property
    def rect_x(self):
        return self._NODESPRITE_DATA["rect"][0]
    @rect_x.setter
    def rect_x(self, v):
        if not isinstance(v, int):
            raise TypeError("Expected integer value.")
        self._NODESPRITE_DATA["rect"][0] = v
        self._NODESPRITE_ValidateRect()

    @property
    def rect_y(self):
        return self._NODESPRITE_DATA["rect"][1]
    @rect_y.setter
    def rect_y(self, v):
        if not isinstance(v, int):
            raise TypeError("Expected integer value.")
        self._NODESPRITE_DATA["rect"][1] = v
        self._NODESPRITE_ValidateRect()


    @property
    def rect_width(self):
        return self._NODESPRITE_DATA["rect"][2]
    @rect_width.setter
    def rect_width(self, v):
        if not isinstance(v, int):
            raise TypeError("Expected integer value.")
        self._NODESPRITE_DATA["rect"][2] = v
        self._NODESPRITE_ValidateRect()


    @property
    def rect_height(self):
        return self._NODESPRITE_DATA["rect"][3]
    @rect_height.setter
    def rect_height(self, v):
        if not isinstance(v, int):
            raise TypeError("Expected integer value.")
        self._NODESPRITE_DATA["rect"][3] = v
        self._NODESPRITE_ValidateRect()

    @property
    def center(self):
        r = self._NODESPRITE_DATA["rect"]
        return (int(r[0] + (r[2] * 0.5)), int(r[1] + (r[3] * 0.5)))

    @property
    def scale(self):
        return (self._NODESPRITE_DATA["scale"][0], self._NODESPRITE_DATA["scale"][1])
    @scale.setter
    def scale(self, scale):
        if not isinstance(scale, (list, tuple)):
            raise TypeError("Expected a list or tuple.")
        if len(scale) != 2:
            raise ValueError("Scale contains wrong number of values.")
        try:
            self.scale_x = scale[0]
            self.scale_y = scale[1]
        except Exception as e:
            raise e

    @property
    def scale_x(self):
        return self._NODESPRITE_DATA["scale"][0]
    @scale_x.setter
    def scale_x(self, v):
        if not isinstance(v, (int, float)):
            raise TypeError("Expected number value.")
        self._NODESPRITE_DATA["scale"][0] = float(v)
        self._NODESPRITE_DATA["scale_dirty"] = True

    @property
    def scale_y(self):
        return self._NODESPRITE_DATA["scale"][1]
    @scale_y.setter
    def scale_y(self, v):
        if not isinstance(v, (int, float)):
            raise TypeError("Expected number value.")
        self._NODESPRITE_DATA["scale"][1] = float(v)
        self._NODESPRITE_DATA["scale_dirty"] = True

    @property
    def image(self):
        return self._NODESPRITE_DATA["image"]
    @image.setter
    def image(self, src):
        src = src.strip()
        if self._NODESPRITE_DATA["image"] == src:
            return # Nothing to change... lol
        if self._NODESPRITE_DATA["image"] != "":
            self._NODESPRITE_DATA["surface"] = None # Clear reference to original surface.
        if src != "":
            rm = self.resource
            try:
                if not rm.has("graphic", src):
                    rm.store("graphic", src)
                self._NODESPRITE_DATA["image"] = src
                self._NODESPRITE_DATA["surface"] = rm.get("graphic", src)
                if self._NODESPRITE_DATA["surface"] is None:
                    self._NODESPRITE_DATA["image"] = ""
                    self._NODESPRITE_DATA["rect"]=[0,0,0,0]
                else:
                    # Resetting the rect to identity for the new image.
                    surf = self._NODESPRITE_DATA["surface"]()
                    size = surf.get_size()
                    self._NODESPRITE_DATA["rect"]=[0,0,size[0], size[1]]
            except Exception as e:
                raise e
        else:
            self._NODESPRITE_DATA["image"] = ""
            self._NODESPRITE_DATA["rect"]=[0,0,0,0]

    def _render(self, surface):
        # Call the on_render() method, if any
        Node2D._callOnRender(self, surface)
        
        # Paint the sprite onto the surface
        if self._NODESPRITE_DATA["surface"] is not None:
            rect = self._NODESPRITE_DATA["rect"]
            scale = self._NODESPRITE_DATA["scale"]
            surf = self._NODESPRITE_DATA["surface"]()
            # Of course, only bother if we have a surface to work with.
            if surf is not None:
                # Do some prescaling work, if needed.
                if self._NODESPRITE_DATA["scale_dirty"]:
                    self._NODESPRITE_UpdateScaleSurface(scale, surf)
                fsurf = surf # Initial assumption that the surface is also the "frame"
                # If we have a "frame" surface, however, let's get it and blit the rect into the frame surface.
                if "frame_surf" in self._NODESPRITE_DATA:
                    fsurf = self._NODESPRITE_DATA["frame_surf"]
                    fsurf.blit(surf, (0, 0), rect) 
                # If scaling, then transform (scale) the frame surface into the scale surface and set the frame surface to the scale surface. 
                if "scale_surf" in self._NODESPRITE_DATA:
                    ssurf = self._NODESPRITE_DATA["scale_surf"]
                    pygame.transform.scale(fsurf, ssurf.get_size(), ssurf)
                    fsurf = ssurf

                # Place the sprite! WHEEEEE!
                pos = self.position
                surface.blit(fsurf, pos)

        # Call on all children
        Node._render(self, surface)


    def _NODESPRITE_UpdateScaleSurface(self, scale, surf):
        self._NODESPRITE_DATA["scale_dirty"] = False
        ssurf = None
        if "scale_surf" in self._NODESPRITE_DATA:
            ssurf = self._NODESPRITE_DATA["scale_surf"]

        if scale[0] == 1.0 and scale[1] == 1.0:
            if ssurf is not None:
                del self._NODESPRITE_DATA["scale_surf"]
            return
        nw = int(self.rect_width * scale[0])
        nh = int(self.rect_height * scale[1])

        if nw != ssurf.get_width() or nh != ssurf.get_height():
            ssurf = pygame.Surface((nw, nh), pygame.SRCALPHA, surf)
            ssurf.fill(pygame.Color(0,0,0,0))
            self._NODESPRITE_DATA["scale_surf"] = ssurf

    def _NODESPRITE_ValidateRect(self):
        if self._NODESPRITE_DATA["surface"] is None:
            self._NODESPRITE_DATA["rect"] = [0,0,0,0]
        else:
            rect = self._NODESPRITE_DATA["rect"]
            isize = (self.image_width, self.image_height)
            if rect[0] < 0:
                rect[2] += rect[0]
                rect[0] = 0
            elif rect[0] >= isize[0]:
                rect[0] = isize[0]-1
                rect[2] = 0
            if rect[1] < 0:
                rect[3] += rect[1]
                rect[1] = 0
            elif rect[1] >= isize[1]:
                rect[1] = isize[1]-1
                rect[3] = 0
            if rect[2] < 0:
                rect[2] = 0
            elif rect[0] + rect[2] > isize[0]:
                rect[2] = isize[0] - rect[0]
            if rect[3] < 0:
                rect[3] = 0
            elif rect[1] + rect[3] > isize[1]:
                rect[3] = isize[1] - rect[1]

            fssize = [0,0]
            if rect[2] > 0 and rect[3] > 0:
                if rect[2] < isize[0] or rect[1] < isize[1]:
                    surf = self._NODESPRITE_DATA["surface"]()
                    self._NODESPRITE_DATA["frame_surf"] = pygame.Surface((rect[2], rect[3]), pygame.SRCALPHA, surf)
            
            if fssize[0] > 0 and fssize[1] > 0:
                pass
            elif "frame_surf" in self._NODESPRITE_DATA:
                del self._NODESPRITE_DATA["frame_surf"]




