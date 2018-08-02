import game.gbe

def start():
    t = game.gbe.Time()
    t.reset()

    d = game.gbe.Display()
    d.init()
    while t.aliveSeconds < 5.0:
        print(t.aliveSeconds)
    d.close()
