#!/usr/bin/env python

import pygame
import math
import funcs
from pygamehelper import PygameHelper

red = (255, 100, 100)
blue= (100, 100, 255)
black = (0, 0, 0)
green = (100, 255, 100)

class S:
    def __init__(self, start, end, color = black):
        self.a = start
        self.b = end
        self.color = color
        self.active = False

class P:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

class Tool:
    def mouseUp(self, button, pos):
        pass

    def activate(self):
        pass

class ToolLine(Tool):
    def __init__(self, wnd):
        self.wnd = wnd

    def activate(self):
        pygame.mouse.set_cursor((8, 8), (4, 4), (24, 24, 24, 231, 231, 24, 24, 24), (0, 0, 0, 0, 0, 0, 0, 0))

    def mouseUp(self, button, pos):
        wnd = self.wnd
        mx, my = pos

        start = None

        for s in wnd.segments:
            a = wnd._project(s.a)
            b = wnd._project(s.b)
            if a and b:
                x0, y0 = wnd._to_zero(a)
                x1, y1 = wnd._to_zero(b)
                if abs(x0-mx) < 5 and abs(y0-my) < 5:
                    start = s.a
                    break
                if abs(x1-mx) < 5 and abs(y1-my) < 5:
                    start = s.b
                    break

        if start:
            self.wnd.segments.append(S(start, P(2, 2, 2)))

class ToolSelect(Tool):
    def __init__(self, wnd):
        self.wnd = wnd

    def activate(self):
        pygame.mouse.set_cursor((16, 19), (0, 0), (128, 0, 192, 0, 160, 0, 144, 0, 136, 0, 132, 0, 130, 0, 129, 0, 128, 128, 128, 64, 128, 32, 128, 16, 129, 240, 137, 0, 148, 128, 164, 128, 194, 64, 2, 64, 1, 128), (128, 0, 192, 0, 224, 0, 240, 0, 248, 0, 252, 0, 254, 0, 255, 0, 255, 128, 255, 192, 255, 224, 255, 240, 255, 240, 255, 0, 247, 128, 231, 128, 195, 192, 3, 192, 1, 128))

    def mouseUp(self, button, pos):
        mx, my = pos
        wnd = self.wnd

        for s in wnd.segments:
            s.active = False

        for s in wnd.segments:
            a = wnd._project(s.a)
            b = wnd._project(s.b)
            if a and b:
                x0, y0 = wnd._to_zero(a)
                x1, y1 = wnd._to_zero(b)
                if funcs.dist(x0, y0, x1, y1, mx, my) < 5:
                    s.active = True
                    break

def put_cube(s, x, y, z, c):
    w = 10
    s.append(S(P(x, y, z), P(x+w, y, z), c))
    s.append(S(P(x, y, z), P(x, y+w, z), c))
    s.append(S(P(x, y+w, z), P(x+w, y+w, z), c))
    s.append(S(P(x+w, y, z), P(x+w, y+w, z), c))

    s.append(S(P(x+w, y, z), P(x+w, y, z+w), c))
    s.append(S(P(x, y+w, z), P(x, y+w, z+w), c))
    s.append(S(P(x, y, z), P(x, y, z+w), c))
    s.append(S(P(x+w, y+w, z), P(x+w, y+w, z+w), c))

    s.append(S(P(x, y, z+w), P(x+w, y, z+w), c))
    s.append(S(P(x, y, z+w), P(x, y+w, z+w), c))
    s.append(S(P(x, y+w, z+w), P(x+w, y+w, z+w), c))
    s.append(S(P(x+w, y, z+w), P(x+w, y+w, z+w), c))

class Starter(PygameHelper):
    def __init__(self):
        self.w, self.h = 800, 600
        PygameHelper.__init__(self, size=(self.w, self.h),
                              fill=((255,255,255)))

        self.D = 500 # distance eye-screen in pixels
        self.camera = P(0, 0, 0)
        self.camera_angle = 0
        self.camera_angle_vert = 0
        self.pressed = set()

        self._set_tool(ToolSelect(self))

        self.segments = []
        put_cube(self.segments, 40, 0, 40, red)
        put_cube(self.segments, -40, 0, 40, green)
        put_cube(self.segments, 40,  0, -40, blue)
        put_cube(self.segments, -40,  0, -40, black)

        # for a in range(0,90,10):
        #     for b in range(0,90,10):
        #         self.segments.append(S(P(a, b, 1), P(a, b, 70000), green))
        #         self.segments.append(S(P(a, 1, b), P(a, 70000, b), blue))
        #         self.segments.append(S(P(1, a, b), P(70000, a, b), red))

        self.segments.append(S(P(-1, 0, 0), P(1, 0, 0)))
        self.segments.append(S(P(0, -1, 0), P(0, 1, 0)))
        self.segments.append(S(P(0, 0, -1), P(0, 0, 1)))

    def _set_tool(self, tool):
        self.tool = tool
        self.tool.activate()

    def _move_camera(self, side, dy, forward):
        a = self.camera_angle
        cos = math.cos
        sin = math.sin
        dx = forward * sin(a) + side * sin(a+3.14/2)
        dz = forward * cos(a) + side * cos(a+3.14/2)

        self.camera.x += dx
        self.camera.y += dy
        self.camera.z += dz

        print ("Camera: ", self.camera.x, self.camera.y, self.camera.z)


    def _project(self, p):
        D = self.D

        x = p.x
        y = p.y
        z = p.z
        
        xu = self.camera.x
        yu = self.camera.y
        zu = self.camera.z

        x = x - xu
        y = y - yu
        z = z - zu

        x, y, z = funcs.rotate(x, y, z,
                               self.camera_angle,
                               self.camera_angle_vert)

        if (z <= 0.0):
            return None

        return [int(D/float(z)*x),
                int(D/float(z)*y)]

    def _draw_segment(self, s):
        a = self._project(s.a)
        b = self._project(s.b)
        if a and b:
            if s.active:
                width=3
            else:
                width=1
            pygame.draw.line(self.screen,
                             s.color,
                             self._to_zero(a),
                             self._to_zero(b),
                             width)

    def _to_zero(self, p):
        x, y = p;
        return [int(x + self.w/2), int(-y + self.h/2)]

    def _draw_zero(self):
        pygame.draw.line(self.screen,
                         (200, 200, 200),
                         [0, int(self.h/2)],
                         [self.w, int(self.h/2)])
        pygame.draw.line(self.screen,
                         (200, 200, 200),
                         [int(self.w/2), 0],
                         [int(self.w/2), self.h])

    def _draw_cam_pos(self):
        pygame.draw.circle(self.screen, red, (int(self.camera.x),
                                              int(self.camera.z)), 2)

    def keyDown(self, key):
        self.pressed.add(key)
        print(key)

    def keyUp(self, key):
        self.pressed.discard(key)

    def mouseUp(self, button, pos):
        self.tool.mouseUp(button, pos)

    def update(self):
        shift_down = False
        if 303 in self.pressed or 304 in self.pressed:
            shift_down = True

        if shift_down:
            if 273 in self.pressed: # up
                self._move_camera(0, 1, 0)
            if 274 in self.pressed: # down
                self._move_camera(0, -1, 0)
        else:
            if 273 in self.pressed: # up
                self._move_camera(0, 0, 1)
            if 274 in self.pressed: # down
                self._move_camera(0, 0, -1)

        if 97 in self.pressed: # A
            self.camera_angle -= 0.03
        if 100 in self.pressed: # D
            self.camera_angle += 0.03
        if 115 in self.pressed: # S
            self.camera_angle_vert -= 0.03
        if 119 in self.pressed: # W
            self.camera_angle_vert += 0.03

        if 275 in self.pressed: # right
            self._move_camera(1, 0, 0)
        if 276 in self.pressed: # left
            self._move_camera(-1, 0, 0)

        if 280 in self.pressed: # page-up
            self.D += 10.0
        if 281 in self.pressed: # page-down
            self.D -= 10.0

        if 108 in self.pressed: # 'L'
            self._set_tool(ToolLine(self))
        if 112 in self.pressed: # 'P'
            self._set_tool(ToolSelect(self))

    def draw(self):
        self.screen.fill((255,255,255))
        self._draw_zero()
        self._draw_cam_pos()
        for s in self.segments:
            self._draw_segment(s)

s = Starter()

s.mainLoop(30)
