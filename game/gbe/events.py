'''
    Filename events.py
    Author: Bryan "ObsidianBlk" Miller
    Date Created: 8/1/2018
    Python Version: 3.7
'''
import time
import weakref
import pygame

def _getWeakRef(fn):
    if not hasattr(fn, "__call__"):
        return None
    if hasattr(fn, "__self__"):
        return weakref.WeakMethod(fn)
    return weakref.ref(fn)


class EventError(Exception):
    pass

class _Events:
    def __init__(self):
        self._signals = {}

    def _ClearUnreferenced(self):
        for signal in self._signals:
            removal = [s for s in self._signals[signal] if s() is None]
            for r in removal:
                self._signals[signal].remove(r)

    def listen(self, signal, fn):
        ref = _getWeakRef(fn)
        if ref is None or ref() is None:
            raise EventError("Expected a function callback.") 
        if not signal in self._signals:
            self._signals[signal] = []
        if not ref in self._signals[signal]:
            self._signals[signal].append(ref)

    def unlisten(self, signal, fn):
        ref = _getWeakRef(fn)
        if res is None or ref() is None:
            return # Not a function. Nothing to do.
        if signal in self._signals:
            if ref in self._signals[signal]:
                self._signals[signal].remove(ref)

    def unlisten_all(self, signal):
        if signal in self._signals:
            del self._signals[signal]

    def emit(self, signal, data):
       if signal in self._signals:
           for r in self._signals[signal]:
                fn = r()
                if fn is not None:
                   fn(signal, data)
       self._ClearUnreferenced()

# Create the actual Events instance :)
Events = _Events()


_ClickDelayMax=500 # in Milliseconds
_DOWNKEYS=[]
_DOWNMBUTTONS=[]
_DOWNJBUTTONS=[]

def _WatchKey(key):
    global _DOWNKEYS
    for k in _DOWNKEYS:
        if k[0] == key:
            return # Already watching. Technically, this should never happen.
    _DOWNKEYS.append((key, int(round(time.time()*1000))))
def _ReleaseKey(key):
    global _DOWNKEYS, _ClickDelayMax
    tick = int(round(time.time()*1000))
    for k in _DOWNKEYS:
        if k[0] == key:
            lastTick = k[1]
            _DOWNKEYS.remove(k)
            if tick - lastTick <= _ClickDelayMax:
                Events.emit("KEYPRESSED", {"key":key, "mod":pygame.key.get_mods(), "key_name":pygame.key.name(key)})
            return # Done.
    # We found nothing, boss.


def _WatchButton(device, button):
    global _DOWNMBUTTONS, _DOWNJBUTTONS
    tick = int(round(time.time()*1000))
    btnsrc = _DOWNMBUTTONS
    if device >= 0:
        btnsrc = _DOWNJBUTTONS
    for b in btnsrc:
        if b[0] == device and b[1] == button:
            return # Already Watching...
    btnsrc.append((device, button, tick))
def _ReleaseButton(device, button):
    global _DOWNMBUTTONS, _DOWNJBUTTONS, _ClickDelayMax
    tick = int(round(time.time()*1000))
    btnsrc = _DOWNMBUTTONS
    if device >= 0:
        btnsrc = _DOWNJBUTTONS
    for b in btnsrc:
        if b[0] == device and b[1] == button:
            lastTick = b[2]
            btnsrc.remove(b)
            if tick - lastTick <= _ClickDelayMax:
                if device >= 0:
                    Events.emit("JOYBUTTONPRESSED", {"joy":device, "button":button})
                else:
                    Events.emit("MOUSEBUTTONPRESSED", {"pos":pygame.mouse.get_pos(), "button":button})
            return # Done.
    # We found nothing, boss.

def pollEmitter():
    global Events, _WatchKey, _ReleaseKey, _WatchButton, _ReleaseButton
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            Events.emit("QUIT", {})
        elif event.type == pygame.KEYDOWN:
            _WatchKey(event.key)
            Events.emit("KEYDOWN", {"unicode":event.unicode, "key":event.key, "mod":event.mod, "key_name":pygame.key.name(event.key)})
        elif event.type == pygame.KEYUP:
            Events.emit("KEYUP", {"key":event.key, "mod":event.mod, "key_name":pygame.key.name(event.key)})
            _ReleaseKey(event.key)
        elif event.type == pygame.MOUSEMOTION: 
            Events.emit("MOUSEMOTION", {"pos":event.pos, "rel":event.rel, "buttons":event.buttons})
        elif event.type == pygame.MOUSEBUTTONUP:
            Events.emit("MOUSEBUTTONUP", {"pos":event.pos, "button":event.button})
            _ReleaseButton(-1, event.button)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            _WatchButton(-1, event.button)
            Events.emit("MOUSEBUTTONDOWN", {"pos":event.pos, "button":event.button})
        elif event.type == pygame.VIDEORESIZE:
            # NOTE: There is a resize bug in Linux. This will stop working after a short time. Grrr
            Events.emit("VIDEORESIZE", {"size":event.size, "w":event.w, "h":event.h})
        elif event.type == pygame.VIDEOEXPOSE:
            Events.emit("VIDEOEXPOSE", {})
        elif event.type == pygame.JOYAXISMOTION:
            Events.emit("JOYAXISMOTION", {"joy":event.joy, "axis":event.axis, "value":event.value})
        elif event.type == pygame.JOYBALLMOTION:
            Events.emit("JOYBALLMOTION", {"joy":event.joy, "ball":event.ball, "res":event.rel})
        elif event.type == pygame.JOYHATMOTION:
            Events.emit("JOYHATMOTION", {"joy":event.joy, "hat":event.hat, "value":event.value})
        elif event.type == pygame.JOYBUTTONUP:
            Events.emit("JOYBUTTONUP", {"joy":event.joy, "button":event.button})
            _ReleaseButton(event.joy, event.button)
        elif event.type == pygame.JOYBUTTONDOWN:
            _WatchButton(event.joy, event.button)
            Events.emit("JOYBUTTONDOWN", {"joy":event.joy, "button":event.button})
        elif event.type == pygame.ACTIVEEVENT:
            if event.state == 1:
                if event.gain == 0:
                    Events.emit("FOCUSLOST", {})
                elif event.gain == 1:
                    Events.emit("FOCUSGAINED", {})
        else:
            if hasattr(event, "code"):
                Events.emit("PYGUSER_{}".format(event.code), {})
            else:
                print("Unkown pygame event type '{}'".format(pygame.event.event_name(event.type)))



