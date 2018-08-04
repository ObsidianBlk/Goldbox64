from . import gbe
from .nodes import *

_RUNNING = False


def _OnVideoResize(event, data):
    flags = gbe.display.Display.flags
    gbe.display.Display.set_mode(data["size"], flags)
    print("Resized to {}".format(gbe.display.Display.resolution))

def _OnKeyEvent(event, data):
    global _RUNNING
    if event == "KEYDOWN":
        if data["key"] == 27:
            _RUNNING = False
        print("Key {} down".format(data["key"]))
    elif event == "KEYUP":
        print("Key {} up".format(data["key"]))
    elif event == "KEYPRESSED":
        print("Key {} pressed".format(data["key"]))



def start():
    global _RUNNING, _OnKeyEvent, _OnVideoResize
    t = gbe.time.Time()
    t.reset()

    gbe.events.Events.listen("KEYDOWN", _OnKeyEvent)
    gbe.events.Events.listen("KEYUP", _OnKeyEvent)
    gbe.events.Events.listen("KEYPRESSED", _OnKeyEvent)
    d = gbe.display.Display
    d.init()
    gbe.events.Events.listen("VIDEORESIZE", _OnVideoResize)

    root = NodeInterface()

    _RUNNING = True
    while _RUNNING:
        gbe.events.pollEmitter()
        d.surface.fill(pygame.Color(0,0,255))
        #pygame.draw.rect(d.surface, pygame.Color(255,0,0), (0,0,20,10), 1)
        root._update(t.delta)
        root._render(d.surface)
        d.flip()
    d.close()
