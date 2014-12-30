from tools import Tool
import pygame

class ToolSelect(Tool):
    def __init__(self, wnd):
        self.wnd = wnd

    def activate(self):
        pygame.mouse.set_cursor((16, 19), (0, 0), (128, 0, 192, 0, 160, 0, 144, 0, 136, 0, 132, 0, 130, 0, 129, 0, 128, 128, 128, 64, 128, 32, 128, 16, 129, 240, 137, 0, 148, 128, 164, 128, 194, 64, 2, 64, 1, 128), (128, 0, 192, 0, 224, 0, 240, 0, 248, 0, 252, 0, 254, 0, 255, 0, 255, 128, 255, 192, 255, 224, 255, 240, 255, 240, 255, 0, 247, 128, 231, 128, 195, 192, 3, 192, 1, 128))

    def mouseUp(self, button, pos):
        if not self.wnd.shift_down():
            self.wnd.select_nothing()

        objects = self.wnd.get_objects_pointed_at(pos[0], pos[1], "sw")
        if objects:
            if self.wnd.shift_down():
                objects[0][0].active = not objects[0][0].active
            else:
                objects[0][0].active = True
