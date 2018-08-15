from . import gbe
from .nodes import *
from . import scenes

_RUNNING = False


def _OnQuit(event, data):
    global _RUNNING
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
        print("Key {} down".format(data["key_name"]))
    elif event == "KEYUP":
        print("Key {} up".format(data["key_name"]))
    elif event == "KEYPRESSED":
        print("Key {} pressed".format(data["key_name"]))



def start():
    global _RUNNING, _OnKeyEvent, _OnQuit, _OnVideoResize
    sm = gbe.statemachine.StateMachine()

    gbe.events.Events.listen("QUIT", _OnQuit)
    #gbe.events.Events.listen("KEYDOWN", _OnKeyEvent)
    #gbe.events.Events.listen("KEYUP", _OnKeyEvent)
    #gbe.events.Events.listen("KEYPRESSED", _OnKeyEvent)
    d = gbe.display.Display
    d.init(640, 480)
    d.caption = "Goldbox 64"
    d.watch_for_resize(True)
    d.set_clear_color(0,0,0)

    #root = NodeInterface()
    #root.scale_to_display = True
    #root.keep_aspect_ratio = True
    #root.align_center = True
    #root.set_surface((64, 64))

    #sprite = gbe.nodes.NodeSprite("Sprite", root)
    #sprite.image = "maptiles/Walls.png"
    #sprite.rect = (48, 32, 16, 16)
    #sprite.position = (20, 20)

    #text = gbe.nodes.NodeText("TextNode", root)
    #text.font_src = "IttyBitty.ttf"
    #text.size = 4
    #text.antialias = False
    #text.text = "ObsidianBlk 123456"
    #text.set_color(255, 64, 128)
    #text.position_y = 30

    sm.register_node(scenes.mainmenu.get())
    sm.register_node(scenes.editor.get())
    sm.activate_node("MAIN_MENU")

    _RUNNING = True
    while _RUNNING:
        gbe.events.pollEmitter()
        sm.update()
        sm.render()
    sm.close()
    d.close()

