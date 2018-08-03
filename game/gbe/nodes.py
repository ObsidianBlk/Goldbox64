

NODETYPE_NODE = "NODE"

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
    def type(self):
        return NODETYPE_NODE

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

        if hasattr(self, "on_render"):
            self.on_render(surface)





class NodeSurface(Node):
    def __init__(self, name="NodeSurface", parent=None, display_ref=None):
        try:
            Node.__init__(self, name, parent)
        except NodeError as e:
            raise e
        self._surface = None
