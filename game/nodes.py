
from .gbe.nodes import *
import pygame

class NodeInterface(NodeSurface):
    def __init__(self, name="Interface", parent=None):
        try:
            NodeSurface.__init__(self, name, parent)
        except NodeError as e:
            raise e

    def on_render(self):
        size = self.resolution
        self.draw_rect((0, 0, size[0], 10), pygame.Color(255,0,0,128), 1)
        self.draw_circle((int(size[0]/2), int(size[1]/2)), 16, pygame.Color(255,0,0,255), 2, pygame.Color(0,255,0,255))

