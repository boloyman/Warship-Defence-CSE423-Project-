import sys
import random
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math

# Window dimensions set kora
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

# Rocket er properties
ROCKET_SIZE = 50
ship_x = WINDOW_WIDTH // 8
ship_y = 50
SQUARE_SPEED = 20

# Falling circle er properties
CIRCLE_RADIUS = 20
plane_arr = []
FALL_SPEED = 5
SPAWN_RATE = 0.01

# Missile er properties
missiles = []
MISSILE_SPEED = 10
MISSILE_WIDTH = 10

# Game state variables
score = 0
lives = 3
game_over = False
paused = False

def draw_points(x, y):
    glPointSize(2)
    glBegin(GL_POINTS)
    glVertex2f(x, y)
    glEnd()


def draw_line(zone, x1, y1, x2, y2):
    dx = x2 - x1
    dy = y2 - y1
    d = 2 * dy - dx
    inc_e = 2 * dy
    inc_ne = 2 * (dy - dx)
    y = y1
    x = x1
    while x < x2:
        og_x, og_y = convert_original(zone, x, y)
        draw_points(og_x, og_y)
        if d > 0:
            d = d + inc_ne
            y += 1
        else:
            d = d + inc_e
        x += 1

def find_zone(x1, y1, x2, y2):
    dx = x2 - x1
    dy = y2 - y1
    zone = -1

    if abs(dx) >= abs(dy):
        if dx >= 0 and dy >= 0:
            zone = 0
        elif dx <= 0 and dy >= 0:
            zone = 3
        elif dx <= 0 and dy <= 0:
            zone = 4
        elif dx >= 0 and dy <= 0:
            zone = 7
    elif abs(dx) < abs(dy):
        if dx >= 0 and dy >= 0:
            zone = 1
        elif dx <= 0 and dy >= 0:
            zone = 2
        elif dx <= 0 and dy <= 0:
            zone = 5
        elif dx >= 0 and dy <= 0:
            zone = 6

    return zone

def convert(zone, x, y):
    if zone == 0:
        return x, y
    elif zone == 1:
        return y, x
    elif zone == 2:
        return y, -x
    elif zone == 3:
        return -x, y
    elif zone == 4:
        return -x, -y
    elif zone == 5:
        return -y, -x
    elif zone == 6:
        return -y, x
    elif zone == 7:
        return x, -y

def convert_original(zone, x, y):
    if zone == 0:
        return x, y
    elif zone == 1:
        return y, x
    elif zone == 2:
        return -y, -x
    elif zone == 3:
        return -x, y
    elif zone == 4:
        return -x, -y
    elif zone == 5:
        return -y, -x
    elif zone == 6:
        return y, -x
    elif zone == 7:
        return x, -y

def midpoint_line(x1, y1, x2, y2):
    zone = find_zone(x1, y1, x2, y2)
    x1, y1 = convert(zone, x1, y1)
    x2, y2 = convert(zone, x2, y2)
    draw_line(zone, x1, y1, x2, y2)

def midpoint_circle(center_x, center_y, r):
    glPointSize(3)
    glBegin(GL_POINTS)
    x = 0
    y = r
    d = 1 - r
    while x <= y:
        glVertex2f(x + center_x, y + center_y)
        glVertex2f(-x + center_x, y + center_y)
        glVertex2f(x + center_x, -y + center_y)
        glVertex2f(-x + center_x, -y + center_y)
        glVertex2f(y + center_x, x + center_y)
        glVertex2f(-y + center_x, x + center_y)
        glVertex2f(y + center_x, -x + center_y)
        glVertex2f(-y + center_x, -x + center_y)

        se = 2 * (x - y) + 5
        e = (2 * x) + 3

        if d >= 0:
            x += 1
            y -= 1
            d += se
        else:
            x += 1
            d += e

    glEnd()

def draw_ship(x, y):
    midpoint_line(x - 30, y, x + 30, y)
    midpoint_line(x - 30, y, x - 10, y - 10)
    midpoint_line(x - 10, y - 10, x + 30, y - 10)
    midpoint_line(x + 30, y - 10, x + 30, y)

    midpoint_line(x - 20, y, x - 20, y + 10)
    midpoint_line(x - 20, y + 10, x - 15, y + 10)
    midpoint_line(x - 15, y + 10, x - 15, y)

    midpoint_line(x - 5, y, x - 5, y + 20)
    midpoint_line(x - 5, y + 20, x + 10, y + 20)
    midpoint_line(x + 10, y + 20, x + 10, y)

    midpoint_line(x + 15, y, x + 15, y + 12)
    midpoint_line(x + 15, y + 12, x + 25, y + 12)
    midpoint_line(x + 25, y + 12, x + 25, y)

def draw_plane(x, y):

    #body
    midpoint_line(x - 30, y,x + 30, y)
    midpoint_line(x + 30, y, x + 30, y + 10)
    midpoint_line(x + 30, y + 10, x - 20, y + 10)
    midpoint_line(x - 20, y + 10, x - 30, y)

    #left wing
    midpoint_line(x - 5, y + 10, x, y - 8)
    midpoint_line(x, y - 8, x + 10, y - 8)
    midpoint_line(x + 10, y - 8, x + 10, y + 5)

    #right wing
    midpoint_line(x - 5, y + 10, x, y + 20)
    midpoint_line(x, y + 20, x + 10, y + 20)
    midpoint_line(x + 10, y + 20, x + 10, y + 10)

    #rudder
    midpoint_line(x + 15, y + 10, x + 25, y + 25)
    midpoint_line(x + 25, y + 25, x + 30, y + 25)
    midpoint_line(x + 30, y + 25, x + 30, y + 10)


def draw_missile(x, y):
    midpoint_circle(x, y, 5)



def display():
    """Display callback rendering er jonno"""
    global game_over, lives, score

    if lives == 0:
        game_over = True  # Lives sesh hole game over hobe

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    # Falling circles draw kora
    for circle in plane_arr:
        draw_plane(circle[0], circle[1])

    # Missiles draw kora
    for missile in missiles:
        draw_missile(missile[0], missile[1])


    draw_ship(ship_x, ship_y)

    # Score o lives top-right corner e dekhano
    glColor3f(1.0, 1.0, 1.0)  # Score er color white thakbe
    glRasterPos2f(WINDOW_WIDTH - 120, WINDOW_HEIGHT - 30)
    lives_text = f"Lives: {lives}"
    for c in lives_text:
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(c))  # Lives er text display

    # Score top-left corner e dekhano
    glColor3f(1.0, 1.0, 1.0)  # Text er color white
    glRasterPos2f(10, WINDOW_HEIGHT - 30)
    score_text = f"Score: {score}"
    for c in score_text:
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(c))  # Score display

    # "Game Over" message dekhano jodi game over hoye thake
    if game_over:
        glColor3f(1.0, 1.0, 1.0)
        glRasterPos2f(WINDOW_WIDTH // 2 - 100, WINDOW_HEIGHT // 2)
        for c in "Game Over":
            glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(c))

        # Restart prompt display kora
        glRasterPos2f(WINDOW_WIDTH // 2 - 150, WINDOW_HEIGHT // 2 - 30)
        for c in "Press R to Restart":
            glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(c))

    glutSwapBuffers()



def update(value):
    """Game er state update kora (rocket, circle, missile movement)"""
    global ship_y, ship_x, plane_arr, missiles, game_over, lives, score, paused

    if game_over or paused:
        return  # Jodi game over hoye thake ba game pause thake, kono update kora jabe na

    # Falling circles move kora leftward
    for circle in plane_arr[:]:
        circle[0] -= FALL_SPEED  # Circle er x position decrease kora
        if circle[0] + CIRCLE_RADIUS < 0:  # Circle screen er baire giye gele remove kora
            lives -= 1
            print(f"Lives Remaining: {lives}")
            plane_arr.remove(circle)

        # Rocket er sathe collision check kora
        if math.sqrt((ship_x - circle[0]) ** 2 + (ship_y - circle[1]) ** 2) < CIRCLE_RADIUS + ROCKET_SIZE // 2:
            game_over = True  # Collision hole game over hobe
            print("Game Over!")
            break

    # Random bhabe new plane spawn kora
    if random.random() < SPAWN_RATE:
        new_plane = [WINDOW_WIDTH, random.randint(250, 450)]
        plane_arr.append(new_plane)  # Falling circles list e add kora

    # Missiles move kora up (horizontal direction e)
    for missile in missiles[:]:
        missile[1] += MISSILE_SPEED
        if missile[1] > WINDOW_WIDTH:
            missiles.remove(missile)

    # Missiles o falling circles er modhe collision check kora
    for missile in missiles[:]:
        for circle in plane_arr[:]:
            distance = math.sqrt((missile[0] - circle[0]) ** 2 + (missile[1] - circle[1]) ** 2)
            if distance < CIRCLE_RADIUS:  # Collision hole
                missiles = [m for m in missiles if m != missile]  # Missile remove kora
                plane_arr = [c for c in plane_arr if c != circle]  # Circle remove kora
                score += 1  # Score barano
                break  # Ekta missile multiple circle e collide na kore

    glutPostRedisplay()  # Display update kora
    glutTimerFunc(24, update, 0)  # Update function abar call kora


# Keyboard input handler (regular keys)
def keyboard(key, x, y):
    """Keyboard input handle kora, spacebar missile fire korbe"""
    global ship_x, ship_y, plane_arr, missiles, game_over, lives, score, paused

    if key == b'\x1b':  # Escape key press hole game bondho hoye jabe
        print('Game Over. Closing er jonno wait kora...')
        sys.exit()

    if key == b' ':  # Spacebar press hole missile fire hobe
        missile = [ship_x, ship_y + ROCKET_SIZE // 2]
        missiles.append(missile)

    if key == b'r' or key == b'R':  # R key press hole game restart hobe
        print("Game restart hochhe...")
        ship_x = WINDOW_WIDTH // 2
        ship_y = 50
        plane_arr = []
        missiles = []
        lives = 3
        score = 0
        game_over = False
        print("Game Start!")
        main()

    if key == b'p' or key == b'P':  # P key press hole game pause/unpause hobe
        paused = not paused  # Pause state toggle kora
        print('Game paused' if paused else 'Game unpaused')


# Special keys (arrows) input handler
def special_input(key, x, y):
    """Special key press handle kora (arrows e rocket move kora)"""
    global ship_x, ship_y

    if key == GLUT_KEY_LEFT:
        ship_x = max(ROCKET_SIZE // 2, ship_x - SQUARE_SPEED)
    elif key == GLUT_KEY_RIGHT:
        ship_x = min(WINDOW_HEIGHT - ROCKET_SIZE // 2, ship_x + SQUARE_SPEED)

    glutPostRedisplay()


# OpenGL initialization function
def init():
    """OpenGL initialization, background color set kora"""
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(0, WINDOW_WIDTH, 0, WINDOW_HEIGHT)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


# Main function
def main():
    """Main function jeikhane OpenGL initialize kora hoy o game loop shuru hoy"""
    print("Game Start!")
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
    glutInitWindowSize(WINDOW_WIDTH, WINDOW_HEIGHT)
    glutCreateWindow(b"Rocket Shooting Game")

    # Callback functions set kora
    glutDisplayFunc(display)
    glutKeyboardFunc(keyboard)
    glutSpecialFunc(special_input)
    glutTimerFunc(25, update, 0)

    init()

    glutMainLoop()


# Game start kora
main()
