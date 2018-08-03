'''
    Filename time.py
    Author: Bryan "ObsidianBlk" Miller
    Date Created: 8/1/2018
    Python Version: 3.7
'''
import time

class Time:
    def __init__(self):
        self._dticks = 0
        self._ldelta = 0
        self._lastTick = 0

    @property
    def delta(self):
        tick = int(round(time.time() * 1000))
        dt = 0
        if self._lastTick > 0:
            dt = tick - self._lastTick
            self._lastTick = tick
            self._ldelta = dt
            self._dticks += dt
        return dt

    @property
    def last_delta(self):
        return self._ldelta

    @property
    def aliveTicks(self):
        tick = int(round(time.time() * 1000))
        dt = 0
        if self._lastTick > 0:
            dt = tick - self._lastTick
        return self._dticks + dt

    @property
    def aliveSeconds(self):
        return self.aliveTicks / 1000.0

    def reset(self):
        self.dticks = 0
        self._lastTick = int(round(time.time() * 1000))


