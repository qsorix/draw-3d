from tools import Tool
import pygame
from colors import *
from objects import S
import funcs
from funcs import vector_from_to, P

class ToolMove(Tool):
    def reset(self):
        self.start = None
        self.end = None
        self.deactivate()

    def activate(self):
        pygame.mouse.set_cursor(*pygame.cursors.broken_x)

    def mouseMotion(self, buttons, pos, rel):
        if not self.start:
            points = self.wnd.get_objects_pointed_at(*pos)
            if points:
                self.wnd.drawn_indicators = [points[0][1]]
            return

        points = self.wnd.get_objects_pointed_at(*pos)
        if points:
            self.end = points[0][1]
            self.wnd.drawn_indicators = [self.start, self.end]
            self.wnd.drawn_segments = [S(self.start, self.end, gray)]

    def mouseUp(self, button, pos):
        if not self.start:
            points = self.wnd.get_objects_pointed_at(*pos)
            if points:
                self.start = points[0][1]
            self.wnd.drawn_indicators = [self.start]

        else:
            if self.start and self.end:
                self.wnd.move_selected(vector_from_to(self.start, self.end))

            self.start = None
            self.end = None
