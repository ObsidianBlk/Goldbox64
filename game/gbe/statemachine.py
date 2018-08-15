
from .events import Events
from .nodes import Node
from .time import Time
from .display import Display

class StateMachineError(Exception):
    pass


# This is the main, active state (Node).
_ACTIVE_STATE = None

# In some cases, the previous state isn't totally shut down, but temporarily put on hold.
# Only the _render() call will be made on hold states.
_HOLD_STATE = None

# List of all states registered into the State Manager.
_STATE_LIST = []

_TIME = Time()


class StateMachine:
    def __init__(self):
        Events.listen("SCENECHANGE", self.on_scenechange)

    def on_scenechange(self, event, params):
        if "scene" in params and "hold" in params:
            self.activate_node(params["scene"], params["hold"])

    def has_node(self, name):
        """
        Returns true if a Node with the given name has been registered in the State List.
        NOTE: This is only going to check the root Node's name, not any other node in the node tree.
        """
        global _STATE_LIST
        for n in _STATE_LIST:
            if n.name == name:
                return True
        return False

    def register_node(self, node):
        """

        """
        if not isinstance(node, Node):
            raise TypeError("Expected a Node instance.")
        # Check if given the root Node. If not, get the root Node.
        if node.parent != None:
            node = node.root
        if self.has_node(node.name):
            raise StateMachineError("State machine already registered node named '{}'. Names must be unique.".format(node.name))
        global _STATE_LIST
        _STATE_LIST.append(node)

    def activate_node(self, name, hold_previous=False):
        """

        """
        global _ACTIVE_STATE, _TIME
        if self.has_node(name):
            if _ACTIVE_STATE is not None:
                if _ACTIVE_STATE.name == name:
                    return
                self._releaseActive(hold_previous)
            self._setActive(name)
            if _ACTIVE_STATE is not None:
                _TIME.reset()


    def _releaseActive(self, hold_previous):
        global _ACTIVE_STATE, _HOLD_STATE
        a = _ACTIVE_STATE
        a._pause()
        if _HOLD_STATE is not None:
            _ACTIVE_STATE = _HOLD_STATE
            _HOLD_STATE = None
            _ACTIVE_STATE._start()
        else:
            _ACTIVE_STATE = None
        
        if hold_previous == True:
            _HOLD_STATE = a
        else:
            a._close()

    def _setActive(self, name):
        global _ACTIVE_STATE, _STATE_LIST
        for n in _STATE_LIST:
            if n.name == name:
                _ACTIVE_STATE = n
                break
        if _ACTIVE_STATE is not None:
            _ACTIVE_STATE._init()
            _ACTIVE_STATE._start()
        elif _HOLD_STATE is not None:
            # If we failed to find an Active state, then we need to drop any hold state as well...
            # Keep things as clean as possible
            _HOLD_STATE._close()
            _HOLD_STATE = None

    def close(self):
        global _ACTIVE_STATE, _HOLD_STATE, _STATE_LIST
        if _HOLD_STATE is not None:
            _HOLD_STATE._close()
            _HOLD_STATE = None
        if _ACTIVE_STATE is not None:
            _ACTIVE_STATE._pause()
            _ACTIVE_STATE._close()
            _ACTIVE_STATE = None
        _STATE_LIST = []

    def update(self):
        global _ACTIVE_STATE, _TIME
        if _ACTIVE_STATE is not None:
            _ACTIVE_STATE._update(_TIME.delta)

    def render(self):
        global _ACTIVE_STATE, _HOLD_STATE
        dsurf = Display.surface
        if dsurf is not None:
            Display.clear()

            # If there's a hold state, render that first.
            if _HOLD_STATE is not None:
                _HOLD_STATE._render(dsurf)
            # Render the active state next so it overdraws the hold state.
            if _ACTIVE_STATE is not None:
                _ACTIVE_STATE._render(dsurf)

            Display.flip()





