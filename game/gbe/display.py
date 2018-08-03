'''
    Filename display.py
    Author: Bryan "ObsidianBlk" Miller
    Date Created: 8/1/2018
    Python Version: 3.7
'''
import pygame

class Display:
    def __init__(self, width=640, height=480):
        self._init = False
        self._resolution = (width, height)
        self._display_surface = None
        self._display_flags = Display.FLAG_RESIZABLE | Display.FLAG_HWSURFACE | Display.FLAG_DOUBLEBUF

    def _isFlagSet(self, flag):
        return (self._display_flags & flag) == flag

    @property
    def surface(self):
        return self._display_surface

    @property
    def width(self):
        if self._display_surface is None:
            return 0
        return self._resolution[0]
    
    @property
    def height(self):
        if self._display_surface is None:
            return 0
        return self._resolution[1]

    @property
    def resolution(self):
        if self._display_surface is None:
            return (0,0)
        return self._display_surface.get_size()

    @property
    def fullscreen(self):
        return self._isFlagSet(Display.FLAG_FULLSCREEN)

    @property
    def double_buffered(self):
        return self._isFlagSet(Display.FLAG_DOUBLEBUF)

    @property
    def resizable(self):
        return self._isFlagSet(Display.FLAG_RESIZABLE)

    @property
    def no_frame(self):
        return self._isFlagSet(Display.FLAG_NOFRAME)

    @property
    def opengl(self):
        return self._isFlagSet(Display.FLAG_OPENGL)

    def toggle_fullscreen(self):
        if self._isFlagSet(Display.FLAG_FULLSCREEN):
            self._display_flags ^= Display.FLAG_FULLSCREEN
        else:
            self._display_flags |= Display.FLAG_FULLSCREEN
        self.set_mode(self._resolution, flags)

    def set_mode(self, resolution, flags):
        if (self._init == False):
            self._init = True
            pygame.init()
        self._display_surface = pygame.display.set_mode(resolution, flags)
        self._display_flags = self._display_surface.get_flags()
        self._resolution = self._display_surface.get_size()
        return self

    def init(self):
        if self._init == False:
            self._init = True
            pygame.init()
            self.set_mode(self._resolution, self._display_flags)
        return self

    def close(self):
        pygame.quit()

    FLAG_SWSURFACE = pygame.SWSURFACE
    FLAG_HWSURFACE = pygame.HWSURFACE
    FLAG_HWPALETTE = pygame.HWPALETTE
    FLAG_DOUBLEBUF = pygame.DOUBLEBUF
    FLAG_FULLSCREEN = pygame.FULLSCREEN
    FLAG_OPENGL = pygame.OPENGL
    FLAG_RESIZABLE = pygame.RESIZABLE
    FLAG_NOFRAME = pygame.NOFRAME


    
