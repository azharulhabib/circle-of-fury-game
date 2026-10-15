# core/camera.py
import math
from OpenGL.GL import *
from OpenGL.GLU import *
from config import WINDOW_W, WINDOW_H, ALLY
from core.game_state import state


class Camera:
    def __init__(self):
        self.angle = -90.0
        self.radius = 700.0
        self.height = 500.0
        self.first_person = False

    def setup(self):
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(80, WINDOW_W / float(WINDOW_H), 0.1, 2500.0)

        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

        if self.first_person:
            target_f = next((f for f in state.fighters if f["state"] == ALLY and f["alive"]), None)
            if target_f is not None:
                gluLookAt(
                    target_f["x"], target_f["y"], 60,
                    0, 0, 120,
                    0, 0, 1
                )
                return

        # Orbit camera
        cx = math.cos(math.radians(self.angle)) * self.radius
        cy = math.sin(math.radians(self.angle)) * self.radius
        cz = self.height

        gluLookAt(cx, cy, cz, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0)

    def rotate(self, delta):
        self.angle += delta

    def adjust_height(self, delta):
        self.height = max(120, min(self.height + delta, 2000))

    def toggle_first_person(self):
        self.first_person = not self.first_person


camera = Camera()