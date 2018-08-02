'''
    Filename core.py
    Author: Bryan "ObsidianBlk" Miller
    Date Created: 8/1/2018
    Python Version: 3.7
'''
import time
import pygame


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





class Display:
    def __init__(self, width=640, height=480):
        self._init = False
        self._resolution = width, height

    @property
    def surface(self):
        return self._display_surface

    @property
    def width(self):
        return self._resolution[0]

    @property
    def height(self):
        return self._resolution[1]

    def init(self):
        if self._init == False:
            self._init = True
            pygame.init()
            self._display_surface = pygame.display.set_mode(self._resolution, pygame.HWSURFACE | pygame.DOUBLEBUF)

    def close(self):
        pygame.quit()

    
