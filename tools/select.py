from tools import Tool
import pygame
from colors import *
import funcs

class ToolSelect(Tool):
    def reset(self):
        self.rect_start = None
        self.deactivate()

    def activate(self):
        pygame.mouse.set_cursor((16, 19), (0, 0), (128, 0, 192, 0, 160, 0, 144, 0, 136, 0, 132, 0, 130, 0, 129, 0, 128, 128, 128, 64, 128, 32, 128, 16, 129, 240, 137, 0, 148, 128, 164, 128, 194, 64, 2, 64, 1, 128), (128, 0, 192, 0, 224, 0, 240, 0, 248, 0, 252, 0, 254, 0, 255, 0, 255, 128, 255, 192, 255, 224, 255, 240, 255, 240, 255, 0, 247, 128, 231, 128, 195, 192, 3, 192, 1, 128))

    def mouseMotion(self, buttons, pos, rel):
        if self.rect_start:
            x = min(self.rect_start[0], pos[0])
            y = min(self.rect_start[1], pos[1])
            w = abs(self.rect_start[0] - pos[0])
            h = abs(self.rect_start[1] - pos[1])
            r = pygame.Rect(x, y, w, h)
            self.wnd.plain_rects = [r]

    def mouseDown(self, button, pos):
        self.rect_start = pos

    def mouseUp(self, button, pos):
        if self.rect_start and self.rect_start != pos:
            x = min(self.rect_start[0], pos[0])
            y = min(self.rect_start[1], pos[1])
            w = abs(self.rect_start[0] - pos[0])
            h = abs(self.rect_start[1] - pos[1])

            ray1 = self.wnd.get_view_ray(x, y)
            ray2 = self.wnd.get_view_ray(x, y+h)
            ray3 = self.wnd.get_view_ray(x+w, y+h)
            ray4 = self.wnd.get_view_ray(x+w, y)

            planes = [funcs.plane_containing_rays(ray1, ray2),
                      funcs.plane_containing_rays(ray2, ray3),
                      funcs.plane_containing_rays(ray3, ray4),
                      funcs.plane_containing_rays(ray4, ray1)]

            if not self.wnd.shift_down():
                self.wnd.select_nothing()

            for o in self.wnd.objects_iter():
                inside = True
                for v in o.vertices_iter():
                    for p in planes:
                        if funcs.dot(p.normal, funcs.vector_from_to(p.p0, v)) < 0:
                            inside = False
                            break
                if inside:
                    o.active = True
        else:
            if not self.wnd.shift_down():
                self.wnd.select_nothing()

            objects = self.wnd.get_objects_pointed_at(pos[0], pos[1], "sw")
            if objects:
                if self.wnd.shift_down():
                    objects[0][0].active = not objects[0][0].active
                else:
                    objects[0][0].active = True

        self.rect_start = None
        self.wnd.plain_rects = []
