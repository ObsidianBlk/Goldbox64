
import weakref
import pygame

def _getWeakRef(fn):
    if not hasattr(fn, "__func__"):
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
        def isempty(r):
            return r() is not None

        for signal, sigs in self._signals:
            self._signals[signal] = filter(isempty, sigs)

    def listen(self, signal, fn):
        ref = _getWeakRef(fn)
        if ref is None or ref() is None:
            raise EventError("Expected a function callback.") 
        if not signal in self._signals:
            self._signals[signal] = []
        if not ref in self._signals[signal]:
            self._signal[signal].append(ref)

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




def pollEmitter():
    for event in pygame.event.get():
        #TODO: For each event obtains, convert it for the above Event dispatcher
        pass




