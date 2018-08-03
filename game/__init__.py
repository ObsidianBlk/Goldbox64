import game.gbe

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
    t = game.gbe.Time()
    t.reset()

    game.gbe.events.Events.listen("KEYDOWN", onKeyEvent)
    game.gbe.events.Events.listen("KEYUP", onKeyEvent)
    game.gbe.events.Events.listen("KEYPRESSED", onKeyEvent)
    d = game.gbe.Display()
    d.init()
    _RUNNING = True
    while _RUNNING:
        game.gbe.events.pollEmitter()
    d.close()
