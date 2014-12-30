from tools import Tool
import pygame
from objects import Wall, S

class ToolWall(Tool):
    def reset(self):
        self.picked_segments = []
        self.deactivate()

    def deactivate(self):
        Tool.deactivate(self)
        self.wnd.select_nothing()

    def _create_wall(self):
        points = []
        points.append(self.picked_segments[0].a)
        for s in self.picked_segments:
            points.append(s.b)

        self.wnd.walls.append(Wall(points))

        self.activate()

    def _add_segment(self, s):
        self.picked_segments.append(s)
        segs = self.picked_segments

        if len(segs) <= 1:
            return

        if segs[-2].a == segs[-1].a:
            segs[-2] = S(segs[-2].b, segs[-2].a)
        if segs[-2].b == segs[-1].b:
            segs[-1] = S(segs[-1].b, segs[-1].a)

        print(segs)

        if len(segs) <= 2:
            return

        if segs[-1].b == segs[0].a:
            self._create_wall()

    def activate(self):
        pygame.mouse.set_cursor(*pygame.cursors.diamond)

        self.picked_segments = []
        for s in self.wnd.segments:
            s.active = False

    def mouseUp(self, button, pos):
        objects = self.wnd.get_objects_pointed_at(pos[0], pos[1], "s")
        if objects:
            s = objects[0][0]
            s.active = True
            self._add_segment(s)
