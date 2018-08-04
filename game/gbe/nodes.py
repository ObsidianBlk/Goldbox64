'''
    Filename nodes.py
    Author: Bryan "ObsidianBlk" Miller
    Date Created: 8/1/2018
    Python Version: 3.7
'''

from .display import Display

class NodeError(Exception):
    pass


class Node:
    def __init__(self, name="Node", parent=None):
        self._parent = None
        self._name = name
        self._children = []
        if parent is not None:
            try:
                self.parent = parent
            except NodeError as e:
                raise e

    @property
    def parent(self):
        return self._parent

    @parent.setter
    def parent(self, new_parent):
        try:
            self.parent_to_node(new_parent)
        except NodeError as e:
            raise e

    @property
    def root(self):
        if self._parent is None:
            return self
        return self._parent.root

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if self._parent is not None:
            if self._parent.get_node(value) is not None:
                raise NodeError("Parent already contains node named '{}'.".format(name))
        self._name = value

    @property
    def full_name(self):
        if self._parent is None:
            return self._name
        return self._parent.full_name + "." + self._name

    @property
    def child_count(self):
        return len(this._children)

    def parent_to_node(self, parent, allow_reparenting=False):
        if not isinstance(value, Node):
            raise NodeError("Node may only parent to another Node instance.")
        if self._parent is None or self._parent != parent:
            if self._parent is not None:
                if allow_Reparenting == False:
                    raise NodeError("Node already assigned a parent Node.")
                if self._parent.remove_node(self) != self:
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
        node._parent = self
        if index < 0 or index >= len(self._children):
            self._children.append(node)
        else:
            self._children.insert(index, node)

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
            if node in self._children:
                self._children.remove(node)
                node._parent = None
                return node
        else:
            raise NodeError("Expected a Node instance or a string.")
        return None


    def get_node(self, name):
        if len(self._children) <= 0:
            return None

        subnames = name.split(".")
        for c in self._children:
            if c.name == subnames[0]:
                if len(subnames) > 1:
                    return c.get_node(".".join(subnames[1:-1]))
                return c
        return None


    def _update(self, dt):
        if hasattr(self, "on_update"):
            self.on_update(dt)

        for c in self._children:
            c._update(dt)

    def _render(self, surface):
        for c in self._children:
            c._render(surface)


class Node2D(Node):
    def __init__(self, name="Node2D", parent=None):
        try:
            Node.__init__(self, name, parent)
        except NodeError as e:
            raise e

    def _render(self, surface):
        Node._render(self, surface)

        if hasattr(self, "on_render"):
            self._ACTIVE_SURF = surface
            self.on_render()
            del self._ACTIVE_SURF

    def blit(self, img, pos=(0,0), rect=None):
        if not hasattr(self, "_ACTIVE_SURF"):
            return
        self._ACTIVE_SURF.blit(img, pos, rect)

    def fill(self, color):
        if not hasattr(self, "_ACTIVE_SURF"):
            return
        self._ACTIVE_SURF.fill(color)

    def draw_lines(points, color, thickness=1, closed=False):
        if not hasattr(self, "_ACTIVE_SURF"):
            return
        pygame.draw.lines(self._ACTIVE_SURF, color, closed, points, thickness)

    def draw_rect(rect, color, thinkness=1):
        if not hasattr(self, "_ACTIVE_SURF"):
            return
        pygame.draw.rect(self._ACTIVE_SURF, color, rect, thickness)

    def draw_ellipse(rect, color, thickness=1, fill_color=None):
        if not hasattr(self, "_ACTIVE_SURF"):
            return
        if fill_color is not None:
            pygame.draw.ellipse(self._ACTIVE_SURF, fill_color, rect)
        if thickness > 0:
            pygame.draw.ellipse(self._ACTIVE_SURF, color, rect, thickness)

    def draw_circle(pos, radius, color, thickness=1, fill_color=None):
        if not hasattr(self, "_ACTIVE_SURF"):
            return
        if fill_color is not None:
            pygame.draw.circle(self._ACTIVE_SURF, fill_color, pos, radius)
        if thickness > 0:
            pygame.draw.circle(self._ACTIVE_SURF, color, pos, radius, thickness)

    def draw_polygon(points, color, thickness=1, fill_color=None):
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
        self._offset = (0.0, 0.0)
        self._scale = (1.0, 1.0)
        self._keepAspectRatio = False
        self._surface = None
        self._tsurface = None
        self.set_surface()

    def _updateTransformSurface(self):
        if self._surface is None:
            return
        if self._scale[0] == 1.0 and self._scale[1] == 1.0:
            self._tsurface = None
        size = self._surface.get_size()
        nw = size[0] * self._scale[0]
        nh = 0
        if self._keepAspectRatio:
            nh = size[1] * self._scale[0]
        else:
            nh = size[1] * self._scale[1]
        self._tsurface = pygame.Surface((nw, nh), pygame.SRCALPHA, self._surface)

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
    def offset(self):
        return self._offset
    @offset.setter(self, offset):
        if not isinstance(offset, tuple):
            raise TypeError("Expected a tuple")
        if len(offset) != 2:
            raise ValueError("Expected tuple of length two.")
        if not isinstance(offset[0], (int, float)) or not isinstance(offset[1], (int, float)):
            raise TypeError("Expected number values.")
        self._offset = (float(offset[0]), float(offset[1]))

    @property
    def offset_x(self):
        return self._offset[0]
    @offset_x.setter
    def offset_x(self, x):
        if not isinstance(x, (int, float)):
            raise TypeError("Expected number value.")
        self._offset = (x, self._offset[1])

    @property
    def offset_y(self):
        return self._offset[1]
    @offset_y.setter
    def offset_y(self, y):
        if not isinstance(y, (int, float)):
            raise TypeError("Expected number value.")
        self._offset = (self._offset[0], y)

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
                self._updateTransformSurface()
        else:
            if not isinstance(r, tuple):
                raise TypeError("Expected a tuple.")
            if len(r) != 2:
                raise ValueError("Expected a tuple of length two.")
            if not isinstance(r[0], int) or not isinstance(r[1], int):
                raise TypeError("Tuple expected to contain integers.")
            if dsurf is not None:
                self._surface = pygame.Surface(resolution, pygame.SRCALPHA, dsurf)
            else:
                self._surface = pygame.Surface(resolution, pygame.SRCALPHA)
            self._updateTransformSurface()

    def _render(self, surface):
        if self._surface is None:
            self.set_surface()
        if self._surface is not None:
            Node2D._render(self, self._surface)
        else:
            Node2D._render(self, surface)
        self._scale_and_blit(surface)


    def _scale_and_blit(self, dest):
        dsize = dest.get_size()
        pos = (int(self._offset[0]), int(self._offset[1]))

        src = self._surface
        if self._tsurface is not None:
            pygame.transform.scale(self._surface, self._tsurface.get_size(), self._tsurface)
            src = self._tsurface
        if ssize[0] == dsize[0] and ssize[1] == dsize[1]:
            dest.blit(src, pos)






