# graphics/models.py
import math
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import glutSolidCube, glutSolidCone
from config import INNER_RADIUS, OUTER_RADIUS, ARENA_SLICES, ALLY
from core.game_state import state


def draw_arena():
    angle_step = (2 * math.pi) / ARENA_SLICES

    glBegin(GL_TRIANGLES)
    for i in range(ARENA_SLICES):
        a1 = i * angle_step
        a2 = (i + 1) * angle_step

        glColor3f(0.9, 0.9, 0.9) if (i % 2 == 0) else glColor3f(0.55, 0.55, 0.55)

        x1i = INNER_RADIUS * math.cos(a1)
        y1i = INNER_RADIUS * math.sin(a1)
        x2i = INNER_RADIUS * math.cos(a2)
        y2i = INNER_RADIUS * math.sin(a2)

        x1o = OUTER_RADIUS * math.cos(a1)
        y1o = OUTER_RADIUS * math.sin(a1)
        x2o = OUTER_RADIUS * math.cos(a2)
        y2o = OUTER_RADIUS * math.sin(a2)

        glVertex3f(x1i, y1i, 0)
        glVertex3f(x1o, y1o, 0)
        glVertex3f(x2o, y2o, 0)

        glVertex3f(x1i, y1i, 0)
        glVertex3f(x2o, y2o, 0)
        glVertex3f(x2i, y2i, 0)
    glEnd()


def draw_spear():
    glPushMatrix()
    glPushMatrix()
    glScalef(3, 3, 50)
    glColor3f(0.55, 0.27, 0.07)
    glutSolidCube(1)
    glPopMatrix()
    glPushMatrix()
    glTranslatef(0, 0, 25)
    glColor3f(0.9, 0.9, 0.9)
    glutSolidCone(3, 15, 10, 10)
    glPopMatrix()
    glPopMatrix()


def draw_shield_model():
    glPushMatrix()
    glScalef(10, 30, 40)
    glColor3f(0.2, 0.8, 1.0)
    glutSolidCube(1)
    glPopMatrix()

    glPushMatrix()
    glTranslatef(2, 0, 0)
    glScalef(8, 20, 30)
    glColor3f(1.0, 1.0, 1.0)
    glutSolidCube(1)
    glPopMatrix()


def draw_gun_model():
    glPushMatrix()
    glColor3f(0.2, 0.2, 0.2)
    glScalef(6, 30, 6)
    glutSolidCube(1)
    glPopMatrix()

    glPushMatrix()
    glTranslatef(0, -10, -5)
    glRotatef(45, 1, 0, 0)
    glScalef(5, 10, 5)
    glutSolidCube(1)
    glPopMatrix()


def draw_bullet():
    glPushMatrix()
    glColor3f(1.0, 1.0, 0.0)
    glScalef(3, 8, 3)
    glutSolidCube(1)
    glPopMatrix()


def draw_boss():
    body_height = 260
    head_radius = 90
    arm_thickness = 35
    torso_half_x = 90

    glPushMatrix()
    glTranslatef(state.boss_x, state.boss_y, state.boss_z)
    glRotatef(state.boss_facing_angle, 0, 0, 1)

    # Torso
    glColor3f(0.35, 0.35, 0.35)
    glPushMatrix()
    glTranslatef(0, 0, body_height * 0.5)
    glScalef(180, 140, body_height)
    glutSolidCube(1)
    glPopMatrix()

    # Head
    glPushMatrix()
    glTranslatef(0, 0, body_height + head_radius * 0.6)
    glColor3f(0.6, 0.1, 0.1)
    gluSphere(state.quadric, head_radius, 24, 24)
    glPopMatrix()

    # Right Arm
    shoulder_z = body_height * 0.75
    glPushMatrix()
    glTranslatef(torso_half_x + 5, 0, shoulder_z)
    glRotatef(state.boss_arm_angle, 1, 0, 0)
    glTranslatef(0, -state.arm_length * 0.5, 0)

    glPushMatrix()
    glScalef(arm_thickness, state.arm_length * 0.9, arm_thickness)
    glColor3f(0.4, 0.1, 0.1)
    glutSolidCube(1)
    glPopMatrix()

    # Cleaver/Blade
    glPushMatrix()
    glTranslatef(0, -state.arm_length * 0.5, 0)
    glScalef(100, 60, 60)
    glColor3f(0.2, 0.2, 0.2)
    glutSolidCube(1)
    glPopMatrix()

    glPopMatrix()

    # Left Arm
    glPushMatrix()
    glTranslatef(-torso_half_x - 5, 0, shoulder_z)
    glTranslatef(0, -state.arm_length * 0.5, 0)
    glScalef(arm_thickness, state.arm_length * 0.8, arm_thickness)
    glColor3f(0.3, 0.1, 0.1)
    glutSolidCube(1)
    glPopMatrix()

    glPopMatrix()


def draw_fighters():
    for f in state.fighters:
        if not f["alive"]:
            continue

        x, y = f["x"], f["y"]
        rad_angle = math.atan2(-y, -x)
        angle_deg = math.degrees(rad_angle) - 90

        glPushMatrix()
        glTranslatef(x, y, 0)
        glRotatef(angle_deg, 0, 0, 1)

        # Body color
        glColor3f(1.0, 0.85, 0.0) if (f["state"] == ALLY) else glColor3f(1.0, 1.0, 0.6)

        # Body
        glPushMatrix()
        glTranslatef(0, 0, 22)
        glScalef(12, 8, 22)
        glutSolidCube(1)
        glPopMatrix()

        # Head
        glPushMatrix()
        glTranslatef(0, 0, 38)
        gluSphere(state.quadric, 6, 12, 12)
        glPopMatrix()

        if f["state"] == ALLY:
            if state.allies_have_gun:
                gun_offset = state.weapon_anim_t * 5 if state.weapon_state == "ATTACKING" else 0
                for sign in (1, -1):
                    glPushMatrix()
                    glTranslatef(sign * 10, 0, 24)
                    glRotatef(-45, 1, 0, 0)
                    glRotatef(-sign * 20, 0, 1, 0)
                    glScalef(4, 4, 16)
                    glutSolidCube(1)
                    glPopMatrix()

                glPushMatrix()
                glTranslatef(0, 15 - gun_offset, 24)
                draw_gun_model()
                if state.weapon_state == "ATTACKING":
                    dist = math.sqrt(x*x + y*y)
                    travel = (dist - 20) * state.weapon_anim_t
                    glPushMatrix()
                    glTranslatef(0, 20 + travel, 0)
                    draw_bullet()
                    glPopMatrix()
                glPopMatrix()

            else:
                # Spear arms & weapon
                arm_rot = -45 - (state.weapon_anim_t * 90) if state.weapon_state == "ATTACKING" else 0
                glPushMatrix()
                glTranslatef(10, 0, 24)
                glRotatef(arm_rot, 1, 0, 0)
                glPushMatrix()
                glScalef(4, 4, 16)
                glutSolidCube(1)
                glPopMatrix()
                if state.weapon_state == "READY":
                    glPushMatrix()
                    glTranslatef(0, 10, -5)
                    glRotatef(-90, 1, 0, 0)
                    draw_spear()
                    glPopMatrix()
                glPopMatrix()

                if state.weapon_state == "ATTACKING":
                    dist = math.sqrt(x*x + y*y)
                    travel = (dist - 20) * state.weapon_anim_t
                    glPushMatrix()
                    glTranslatef(0, travel, 120 * state.weapon_anim_t)
                    glRotatef(-90, 1, 0, 0)
                    glRotatef(-15, 1, 0, 0)
                    draw_spear()
                    glPopMatrix()

                glColor3f(1.0, 0.85, 0.0)
                glPushMatrix()
                glTranslatef(-10, 0, 24)
                glScalef(4, 4, 16)
                glutSolidCube(1)
                glPopMatrix()

                if state.allies_have_shield:
                    glPushMatrix()
                    glTranslatef(-15, 5, 20)
                    glRotatef(15, 0, 1, 0)
                    draw_shield_model()
                    glPopMatrix()
        else:
            for sign in (-1, 1):
                glPushMatrix()
                glTranslatef(sign * 10, 0, 24)
                glScalef(4, 4, 16)
                glutSolidCube(1)
                glPopMatrix()

        # Animated legs
        leg_angle = math.sin(math.radians(state.walk_phase)) * 25 if f["moving"] else 0
        for sign, mult in ((-4, 1), (4, -1)):
            glPushMatrix()
            glTranslatef(sign, 0, 14)
            glRotatef(mult * leg_angle, 1, 0, 0)
            glTranslatef(0, 0, -8)
            glScalef(4, 4, 14)
            glutSolidCube(1)
            glPopMatrix()

        glPopMatrix()