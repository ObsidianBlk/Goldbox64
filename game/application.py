
import time
import pygame
from pygame.locals import *

class Application:
    def __init__(self, width=640, height=480):
        self._running = False
        self._init = False
        self._resolution = width, height
        self.lastFrameTime = 0

    def init(self):
        pygame.init()
        self._display_surface = pygame.display.set_mode(self._resolution, pygame.HWSURFACE | pygame.DOUBLEBUF)
        self._init = True

    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False

    def on_cleanup(self):
        pygame.quit()

    def execute(self):
        # We want to automatically exit if app is already running or if app hasn't yet been init.
        if self._running or not self._init:
            return False
        self._running = True

        while self._running:
            # Calculate delta time since last frame.
            currentTime = time.time()
            dt = 0
            if self.lastFrameTime != 0:
                dt = currentTime - self.lastFrameTime
            self.lastFrameTime = currentTime

            for event in pygame.event.get():
                self.on_event(event)
        self.on_cleanup()
