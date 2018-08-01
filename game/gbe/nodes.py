

NODETYPE_NODE = "NODE"

class NodeError(Exception):
    pass


class Node:
    def __init__(self, name="Node", parent=None):
        self._children = []
        self.name = name

    @property
    def type(self):
        return NODETYPE_NODE

    @property
    def parent(self):
        return self._parent

    @parent.setter
    def parent(self, value):
        try:
            self.parent_to_node(value)
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
        if self._parent is None:
            self._parent = value
        elif self._parent != value:
            if allow_Reparenting == False:
                raise NodeError("Node already assigned a parent Node.")
            if self._parent.remove_node(self) != self:
                raise NodeError("Failed to remove self from current parent.")
            parent.attach_node(self)


    def attach_node(self, node, reparent=False, index=-1):
        if node.parent is not None:
            if node.parent == self:
                return # Nothing to do. Given node already parented to this node.
            if reparent = False:
                raise NodeError("Node already parented.")
            if node.parent.remove_node(node) != node:
                raise NodeError("Failed to remove given node from it's current parent.")
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




