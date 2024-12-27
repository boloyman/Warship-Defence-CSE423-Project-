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
rocket_x = WINDOW_WIDTH // 8  # Rocket er initial x position
rocket_y = 50  # Rocket er initial y position
SQUARE_SPEED = 20  # Rocket er movement speed

# Falling circle er properties
CIRCLE_RADIUS = 20
falling_circles = []  # Falling circles array store korbe
FALL_SPEED = 5  # Falling circle er speed
SPAWN_RATE = 0.02  # Falling circle spawn hobar chance pratyek frame e

# Missile er properties
missiles = []  # Missile array store korbe
MISSILE_SPEED = 10  # Missile er movement speed
MISSILE_WIDTH = 10  # Missile er width

# Game state variables
score = 0  # Initial score
lives = 3  # Starting lives
game_over = False  # Game over state
paused = False  # Paused state


# Function to draw rocket (square)
def draw_square(x, y, size):
    """Rocket (square) draw kora jekhane x, y position dewa thakbe"""
    glColor3f(1.0, 1.0, 1.0)  # Rocket er color white hobe
    half_size = size // 2  # Half size calculate kora for centering

    glBegin(GL_QUADS)  # Square shape draw korte GL_QUADS use kora
    glVertex2f(x - half_size, y - half_size)  # Left bottom corner
    glVertex2f(x + half_size, y - half_size)  # Right bottom corner
    glVertex2f(x + half_size, y + half_size)  # Right top corner
    glVertex2f(x - half_size, y + half_size)  # Left top corner
    glEnd()  # End of drawing square


# Function to draw a falling circle
def draw_circle(x, y, radius):
    """Falling circle draw kora, position (x, y) diye radius set kora"""
    glColor3f(1.0, 0.0, 0.0)  # Circle er color red hobe
    glBegin(GL_POLYGON)  # Polygon shape draw korbo (circle er approximation)
    for angle in range(360):  # 360 degree cover kore ekta full circle banano
        rad = math.radians(angle)  # Angle ke radians e convert kora
        xx = x + radius * math.cos(rad)  # x coordinate calculate
        yy = y + radius * math.sin(rad)  # y coordinate calculate
        glVertex2f(xx, yy)  # Each point of the circle draw kora
    glEnd()


# Function to draw missile
def draw_missile(x, y):
    """Missile draw kora, position (x, y) diye"""
    glColor3f(0.0, 1.0, 0.0)  # Missile er color green hobe
    radius = MISSILE_WIDTH // 2  # Missile er radius calculate

    glBegin(GL_POLYGON)  # Polygon shape draw kora
    for angle in range(360):  # 360 degree cover kore ekta full circle banano
        rad = math.radians(angle)  # Angle ke radians e convert kora
        xx = x + radius * math.cos(rad)  # x coordinate calculate
        yy = y + radius * math.sin(rad)  # y coordinate calculate
        glVertex2f(xx, yy)  # Missile er points draw kora
    glEnd()


# Display function - game er UI display kore
def display():
    """Display callback rendering er jonno"""
    global game_over, lives, score

    if lives == 0:
        game_over = True  # Lives sesh hole game over hobe

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)  # Screen clear kora (background refresh)
    glLoadIdentity()  # Identity matrix load kora, OpenGL er transformation er jonno

    # Falling circles draw kora
    for circle in falling_circles:
        draw_circle(circle[0], circle[1], CIRCLE_RADIUS)

    # Missiles draw kora
    for missile in missiles:
        draw_missile(missile[0], missile[1])

    # Rocket draw kora
    draw_square(rocket_x, rocket_y, ROCKET_SIZE)

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

    glutSwapBuffers()  # Double buffering use kore frame swap kora


# Game logic update korar function
def update(value):
    """Game er state update kora (rocket, circle, missile movement)"""
    global rocket_y, rocket_x, falling_circles, missiles, game_over, lives, score, paused

    if game_over or paused:
        return  # Jodi game over hoye thake ba game pause thake, kono update kora jabe na

    # Falling circles move kora leftward
    for circle in falling_circles[:]:
        circle[0] -= FALL_SPEED  # Circle er x position decrease kora
        if circle[0] + CIRCLE_RADIUS < 0:  # Circle screen er baire giye gele remove kora
            lives -= 1  # Life komano
            print(f"Lives Remaining: {lives}")  # Remaining lives print kora
            falling_circles.remove(circle)  # Circle ke list theke remove kora

        # Rocket er sathe collision check kora
        if math.sqrt((rocket_x - circle[0]) ** 2 + (rocket_y - circle[1]) ** 2) < CIRCLE_RADIUS + ROCKET_SIZE // 2:
            game_over = True  # Collision hole game over hobe
            print("Game Over!")  # Game over print kora
            break

    # Random bhabe new circle spawn kora
    if random.random() < SPAWN_RATE:
        new_circle = [WINDOW_WIDTH, random.randint(CIRCLE_RADIUS, WINDOW_HEIGHT - CIRCLE_RADIUS)]
        falling_circles.append(new_circle)  # Falling circles list e add kora

    # Missiles move kora up (horizontal direction e)
    for missile in missiles[:]:
        missile[0] += MISSILE_SPEED  # Missile er x position increase kora
        if missile[0] > WINDOW_WIDTH:  # Missile screen theke baire giye gele remove kora
            missiles.remove(missile)

    # Missiles o falling circles er modhe collision check kora
    for missile in missiles[:]:
        for circle in falling_circles[:]:
            distance = math.sqrt((missile[0] - circle[0]) ** 2 + (missile[1] - circle[1]) ** 2)
            if distance < CIRCLE_RADIUS:  # Collision hole
                missiles = [m for m in missiles if m != missile]  # Missile remove kora
                falling_circles = [c for c in falling_circles if c != circle]  # Circle remove kora
                score += 1  # Score barano
                break  # Ekta missile multiple circle e collide na kore

    glutPostRedisplay()  # Display update kora
    glutTimerFunc(24, update, 0)  # Update function abar call kora


# Keyboard input handler (regular keys)
def keyboard(key, x, y):
    """Keyboard input handle kora, spacebar missile fire korbe"""
    global rocket_x, rocket_y, falling_circles, missiles, game_over, lives, score, paused

    if key == b'\x1b':  # Escape key press hole game bondho hoye jabe
        print('Game Over. Closing er jonno wait kora...')
        sys.exit()

    if key == b' ':  # Spacebar press hole missile fire hobe
        missile = [rocket_x, rocket_y + ROCKET_SIZE // 2]  # Missile rocket er position theke fire hobe
        missiles.append(missile)  # Missile list e add kora

    if key == b'r' or key == b'R':  # R key press hole game restart hobe
        print("Game restart hochhe...")
        rocket_x = WINDOW_WIDTH // 2  # Rocket position reset kora
        rocket_y = 50  # Rocket position reset kora
        falling_circles = []  # Falling circles array clear kora
        missiles = []  # Missile array clear kora
        lives = 3  # Lives reset kora
        score = 0  # Score reset kora
        game_over = False  # Game over reset kora
        print("Game Start!")  # Restart hoye game start kora
        main()

    if key == b'p' or key == b'P':  # P key press hole game pause/unpause hobe
        paused = not paused  # Pause state toggle kora
        print('Game paused' if paused else 'Game unpaused')


# Special keys (arrows) input handler
def special_input(key, x, y):
    """Special key press handle kora (arrows e rocket move kora)"""
    global rocket_x, rocket_y

    if key == GLUT_KEY_DOWN:  # Down arrow key press hole rocket down move korbe
        rocket_y = max(ROCKET_SIZE // 2, rocket_y - SQUARE_SPEED)  # Rocket move down (limit set)
    elif key == GLUT_KEY_UP:  # Up arrow key press hole rocket up move korbe
        rocket_y = min(WINDOW_HEIGHT - ROCKET_SIZE // 2, rocket_y + SQUARE_SPEED)  # Rocket move up

    glutPostRedisplay()  # Display update kora


# OpenGL initialization function
def init():
    """OpenGL initialization, background color set kora"""
    glClearColor(0.0, 0.0, 0.0, 1.0)  # Background color black
    glMatrixMode(GL_PROJECTION)  # Projection matrix set kora
    glLoadIdentity()  # Identity matrix load kora
    gluOrtho2D(0, WINDOW_WIDTH, 0, WINDOW_HEIGHT)  # 2D orthographic projection set kora

    glMatrixMode(GL_MODELVIEW)  # Modelview matrix set kora
    glLoadIdentity()  # Identity matrix load kora


# Main function
def main():
    """Main function jeikhane OpenGL initialize kora hoy o game loop shuru hoy"""
    print("Game Start!")  # Game start message
    glutInit(sys.argv)  # Initialize GLUT
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)  # Double buffering and RGB mode set kora
    glutInitWindowSize(WINDOW_WIDTH, WINDOW_HEIGHT)  # Window size set kora
    glutCreateWindow(b"Rocket Shooting Game")  # Game window create kora

    # Callback functions set kora
    glutDisplayFunc(display)
    glutKeyboardFunc(keyboard)
    glutSpecialFunc(special_input)
    glutTimerFunc(25, update, 0)  # Update loop shuru kora

    init()  # OpenGL initialization call kora

    glutMainLoop()  # GLUT main loop


# Game start kora
main()
