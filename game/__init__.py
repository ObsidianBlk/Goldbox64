from . import gbe

_RUNNING = False


def onKeyEvent(event, data):
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
    global _RUNNING, onKeyEvent
    t = gbe.time.Time()
    t.reset()

    gbe.events.Events.listen("KEYDOWN", onKeyEvent)
    gbe.events.Events.listen("KEYUP", onKeyEvent)
    gbe.events.Events.listen("KEYPRESSED", onKeyEvent)
    d = gbe.display.Display()
    d.init()
    _RUNNING = True
    while _RUNNING:
        gbe.events.pollEmitter()
    d.close()
