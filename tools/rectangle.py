from tools import Tool
import pygame
import funcs
from colors import *
from funcs import vector_from_to
from objects import Wall, S

class ToolRectangle(Tool):
    def reset(self):
        self.start = None
        self.end = None
        self.drawing_plane = None
        self.side_vector = None
        self.deactivate()

    def _put_rectangle(self):
        for s in self._make_rectangle(self.start, self.end, self.side_vector):
            self.wnd.add_segment(s)

    def _make_rectangle(self, start, end, v):
        res = []
        res.append(S(start, start+v))
        res.append(S(start+v, end))
        res.append(S(end, end-v))
        res.append(S(end-v, start))
        return res

    def activate(self):
        pygame.mouse.set_cursor((8, 8), (4, 4), (24, 24, 24, 231, 231, 24, 24, 24), (0, 0, 0, 0, 0, 0, 0, 0))

    def mouseMotion(self, buttons, pos, rel):
        points = self.wnd.get_objects_pointed_at(*pos)

        if not self.start:
            if points:
                self.wnd.drawn_indicators = [points[0][1]]
            return

        if points:
            end = points[0][1]
        else:
            return

        self.end = end

        if not self.drawing_plane:
            self.drawing_plane = self.wnd.pick_plane_facing_camera()

        v = funcs.get_axes_oriented_projection(self.drawing_plane, vector_from_to(self.start, end))
        self.side_vector = v

        self.wnd.drawn_segments = [S(self.start, end, gray)]
        self.wnd.drawn_segments.extend(self._make_rectangle(self.start,
                                                            self.end,
                                                            self.side_vector))
        self.wnd.drawn_indicators = [self.start, end]

    def mouseUp(self, button, pos):
        if not self.start:
            objects = self.wnd.get_objects_pointed_at(*pos, type="wps")
            if objects:
                self.start = objects[0][1]
                if isinstance(objects[0][0], Wall):
                    self.drawing_plane = objects[0][0].plane()
            return

        if self.start and self.end:
            self._put_rectangle()
            self.start = None
            self.end = None
            self.side_vector = None
            self.wnd.drawn_segments = []
            self.wnd.drawn_indicators = []
