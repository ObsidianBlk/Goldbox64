'''
    Filename display.py
    Author: Bryan "ObsidianBlk" Miller
    Date Created: 8/1/2018
    Python Version: 3.7
'''
import pygame
import weakref

class Flag:
    SWSURFACE = pygame.SWSURFACE
    HWSURFACE = pygame.HWSURFACE
    HWPALETTE = pygame.HWPALETTE
    DOUBLEBUF = pygame.DOUBLEBUF
    FULLSCREEN = pygame.FULLSCREEN
    OPENGL = pygame.OPENGL
    RESIZABLE = pygame.RESIZABLE
    NOFRAME = pygame.NOFRAME

    def isSet(flags, flag):
        return (flags & flag) == flag

class _Display:
    def __init__(self, width=0, height=0):
        # NOTE: In the newest version of pygame, setting resolution to 0,0 should set the resolution to that of the screen... so we'll just mimic that.
        self._init = False
        self._resolution = (width, height)
        self._display_surface = None
        self._display_flags = Flag.RESIZABLE | Flag.HWSURFACE | Flag.DOUBLEBUF

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
    def flags(self):
        return self._display_flags

    @property
    def fullscreen(self):
        return Flag.isSet(self._display_flags, Flag.FULLSCREEN)

    @property
    def double_buffered(self):
        return Flag.isSet(self._display_flags, Flag.DOUBLEBUF)

    @property
    def resizable(self):
        return Flag.isSet(self._display_flags, Flag.RESIZABLE)

    @property
    def no_frame(self):
        return Flag.isSet(self._display_flags, Flag.NOFRAME)

    @property
    def opengl(self):
        return Flag.isSet(self._display_flags, Flag.OPENGL)

    def toggle_fullscreen(self):
        if self._isFlagSet(Flag.FULLSCREEN):
            self._display_flags ^= Flag.FULLSCREEN
        else:
            self._display_flags |= Flag.FULLSCREEN
        self.set_mode(self._resolution, flags)

    def set_mode(self, resolution, flags):
        if (self._init == False):
            self._init = True
            pygame.init()
        self._display_surface = pygame.display.set_mode(resolution, flags)
        self._display_flags = self._display_surface.get_flags()
        self._resolution = self._display_surface.get_size()
        return self

    def flip(self):
        if self._init:
            pygame.display.flip()

    def init(self):
        if self._init == False:
            self._init = True
            pygame.init()
            self.set_mode(self._resolution, self._display_flags)
        return self

    def close(self):
        pygame.quit()

# Creating an instance of the _Display class. Really, this game engine is only going to use ONE display.
Display=_Display()



