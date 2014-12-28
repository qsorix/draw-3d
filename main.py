import pygame
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

class P:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

class Starter(PygameHelper):
    def __init__(self):
        self.w, self.h = 800, 600
        PygameHelper.__init__(self, size=(self.w, self.h),
                              fill=((255,255,255)))

        self.D = 50 # distance eye-screen in pixels
        self.camera = P(0, 0, 0)
        self.camera_angle = 0
        self.pressed = set()

        self.segments = []
        self.segments.append(S(P(20, 20, 20), P(30, 20, 20), red))
        self.segments.append(S(P(20, 20, 20), P(20, 30, 20), red))
        self.segments.append(S(P(20, 30, 20), P(30, 30, 20), red))
        self.segments.append(S(P(30, 20, 20), P(30, 30, 20), red))

        self.segments.append(S(P(30, 20, 20), P(30, 20, 30)))
        self.segments.append(S(P(20, 30, 20), P(20, 30, 30)))
        self.segments.append(S(P(20, 20, 20), P(20, 20, 30)))
        self.segments.append(S(P(30, 30, 20), P(30, 30, 30)))

        self.segments.append(S(P(20, 20, 30), P(30, 20, 30), blue))
        self.segments.append(S(P(20, 20, 30), P(20, 30, 30), blue))
        self.segments.append(S(P(20, 30, 30), P(30, 30, 30), blue))
        self.segments.append(S(P(30, 20, 30), P(30, 30, 30), blue))

        self.segments.append(S(P(0, 0, 1), P(0, 0, 70000), green))
        self.segments.append(S(P(0, 0, 1), P(0, 70000, 1), blue))
        self.segments.append(S(P(0, 0, 1), P(70000, 0, 1), red))

    def _project(self, p):
        D = self.D
        x = p.x - self.camera.x
        y = p.y - self.camera.y
        z = p.z - self.camera.z

        if (z <= 0.0):
            return None

        return [int(D/float(z)*x),
                int(D/float(z)*y)]

    def _draw_segment(self, s):
        a = self._project(s.a)
        b = self._project(s.b)
        if a and b:
            pygame.draw.line(self.screen,
                             s.color,
                             self._to_zero(a),
                             self._to_zero(b))

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

    def keyDown(self, key):
        self.pressed.add(key)
        print(key)

    def keyUp(self, key):
        self.pressed.discard(key)

    def update(self):
        shift_down = False
        if 303 in self.pressed or 304 in self.pressed:
            shift_down = True

        if shift_down:
            if 273 in self.pressed: # up
                self.camera.z += 1.0
            if 274 in self.pressed: # down
                self.camera.z -= 1.0
        else:
            if 273 in self.pressed: # up
                self.camera.y += 1.0
            if 274 in self.pressed: # down
                self.camera.y -= 1.0

        if 275 in self.pressed: # right
            self.camera.x += 1.0
        if 276 in self.pressed: # left
            self.camera.x -= 1.0

        if 280 in self.pressed: # page-up
            self.D += 10.0
            print(self.D)
        if 281 in self.pressed: # page-down
            self.D -= 10.0
            print(self.D)

    def mouseUp(self, button, pos):
        if not self.new_start:
            self.new_start = pos
        else:
            self.new_end = pos

            self.segments.append(
                Segment(self.new_start[0], self.new_start[1],
                        self.new_end[0], self.new_end[1]))
            self.intersections = \
                    find_intersections(self.segments)

            self.new_start = None
            self.new_end = None


    def draw(self):
        self.screen.fill((255,255,255))
        self._draw_zero()
        for s in self.segments:
            self._draw_segment(s)

s = Starter()

s.mainLoop(30)
