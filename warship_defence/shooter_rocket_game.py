import sys
import random
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math

# Window er dimensions
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

# Rocket er properties
ROCKET_SIZE = 50
rocket_x = WINDOW_WIDTH // 2
rocket_y = 50
SQUARE_SPEED = 20

# Falling circle er properties
CIRCLE_RADIUS = 20
falling_circles = []
FALL_SPEED = 5
SPAWN_RATE = 0.02  # Probabilty je ekta notun circle spawn hobe prottek frame e

# Missile er properties
missiles = []
MISSILE_SPEED = 10
MISSILE_WIDTH = 10

# Game er state
score = 0  # Score start
lives = 3
game_over = False
paused=False


def draw_square(x, y, size):
    """Square draw kore (x, y) position e."""
    glColor3f(1.0, 1.0, 1.0)  # Rocket er jonno white color
    half_size = size // 2

    # Square draw korte points use kore
    glBegin(GL_POINTS)
    
    # Square er char corner draw kore
    for dx in [half_size, -half_size]:
        for dy in [half_size, -half_size]: 
            glVertex2f(x + dx, y + dy)
    
    # Square er edges er modhe points draw kore (optional)
    for i in range(-half_size, half_size + 1):  # Horizontal edges
        glVertex2f(x + i, y + half_size)  # Top edge
        glVertex2f(x + i, y - half_size)  # Bottom edge
    for i in range(-half_size, half_size + 1):  # Vertical edges
        glVertex2f(x + half_size, y + i)  # Right edge
        glVertex2f(x - half_size, y + i)  # Left edge

    glEnd()

def draw_circle(x, y, radius):
    """Circle draw kore (x, y) position e diye given radius shoho."""
    glColor3f(1.0, 0.0, 0.0)  # Falling circle er jonno red color
    glBegin(GL_POINTS)
    glVertex2f(x, y)  # Circle er center
    for angle in range(360):  # 360 degree coverage
        rad = math.radians(angle)
        xx=x+radius*math.cos(rad)
        yy=y+radius*math.sin(rad)
        glVertex2f(xx,yy)
    glEnd()

def draw_missile(x, y):
    """Missile draw kore (x, y) position e round shape hisebe."""
    glColor3f(0.0, 1.0, 0.0)  # Missile er jonno green color
    radius = MISSILE_WIDTH // 2  # Missile er radius, width er aadha
    glBegin(GL_POINTS)
    glVertex2f(x, y)  # Circle er center
    for angle in range(360):  # 360 degree coverage
        rad = math.radians(angle)
        xx=x+radius*math.cos(rad)
        yy=y+radius*math.sin(rad)
        glVertex2f(xx,yy)
    glEnd()

def display():
    """Display callback jeita rendering kore."""
    global game_over, lives, score

    if lives == 0:
        game_over = True

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    # Falling circles draw kore
    for circle in falling_circles:
        draw_circle(circle[0], circle[1], CIRCLE_RADIUS)

    # Missiles draw kore
    for missile in missiles:
        draw_missile(missile[0], missile[1])

    # Rocket draw kore
    draw_square(rocket_x, rocket_y, ROCKET_SIZE)

    # Top-right corner e remaining lives dekhano
    glColor3f(1.0, 1.0, 1.0)  # Text er jonno white color
    glRasterPos2f(WINDOW_WIDTH - 120, WINDOW_HEIGHT - 30)  # Lives er text er position
    lives_text = f"Lives: {lives}"
    for c in lives_text:
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(c))

    # Top-left corner e score dekhano
    glColor3f(1.0, 1.0, 1.0)
    glRasterPos2f(10, WINDOW_HEIGHT - 30)  # Score er position
    score_text = f"Score: {score}"
    for c in score_text:
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(c))

    # Game over message dekhano jodi game over hoye
    if game_over:
        glColor3f(1.0, 1.0, 1.0)
        glRasterPos2f(WINDOW_WIDTH // 2 - 100, WINDOW_HEIGHT // 2)
        for c in "Game Over":
            glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(c))
        # Restart prompt
        glRasterPos2f(WINDOW_WIDTH // 2 - 150, WINDOW_HEIGHT // 2 - 30)
        for c in "Press R to Restart":
            glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(c))

    glutSwapBuffers()

def update(value):
    """Game logic er update callback."""
    global rocket_y, rocket_x, falling_circles, missiles, game_over, lives, score,paused

    if game_over or paused:
        return  # Jodi game over hoye thake, tahole update bandho

    # Circles ke niche move kora
    for circle in falling_circles[:]:
        circle[1] -= FALL_SPEED
        # Circles remove kora jodi screen er niche pore
        if circle[1] + CIRCLE_RADIUS < 0:
            lives -= 1
            print('Lives Remaining:', lives)
            falling_circles.remove(circle)

        # Rocket er shathe collision check kore
        if math.sqrt((rocket_x - circle[0]) ** 2 + (rocket_y - circle[1]) ** 2) < CIRCLE_RADIUS + ROCKET_SIZE // 2:
            # Collision detect korle game over hoye jabe
            game_over = True
            break

    # Notun circles randomly spawn kore
    if random.random() < SPAWN_RATE:
        new_circle = [random.randint(CIRCLE_RADIUS, WINDOW_WIDTH - CIRCLE_RADIUS), WINDOW_HEIGHT]
        falling_circles.append(new_circle)

    # Missiles ke upar move kore
    for missile in missiles[:]:
        missile[1] += MISSILE_SPEED
        # Missiles remove kora jodi screen theke bahir hoye
        if missile[1] > WINDOW_HEIGHT:
            missiles.remove(missile)

    # Missile er shathe circles er collision check kore
    for missile in missiles[:]:
        for circle in falling_circles[:]:
            distance = math.sqrt((missile[0] - circle[0]) ** 2 + (missile[1] - circle[1]) ** 2)
            if distance < CIRCLE_RADIUS:  # Collision detect
                # Missile o circle ke remove kore
                missiles = [m for m in missiles if m != missile]
                falling_circles = [c for c in falling_circles if c != circle]
                score += 1  # Score barate thake
                break  # Ekta missile e multiple circles check kora theke bachao

    glutPostRedisplay()
    glutTimerFunc(24, update, 0)  # Update loop abar start kore

def keyboard(key, x, y):
    """Regular key press er jonno callback (spacebar er jonno)."""
    global rocket_x, rocket_y, falling_circles, missiles, game_over, lives, score,paused

    if key == b'\x1b':  # Escape key press hole program bondho
        print('Game Over. Waiting to close...')
        sys.exit()
    
    if key == b' ':  # Spacebar press hole missile fire kore
        missile = [rocket_x, rocket_y + ROCKET_SIZE // 2]
        missiles.append(missile)

    if key == b'r' or key == b'R':  # R key press hole game restart hobe
        print("Restarting the game...")
        # game abar suru
        rocket_x = WINDOW_WIDTH // 2
        rocket_y = 50
        falling_circles = []
        missiles = []
        lives = 3
        score = 0
        game_over = False
        main()
    if key ==b'p' or key ==b'P':
        print('pausing The game')
        paused = not paused

def special_input(key, x, y):
    """Arrow key er jonno special keys callback."""
    global rocket_x, rocket_y

    if key == GLUT_KEY_UP:
        rocket_y = min(WINDOW_HEIGHT - ROCKET_SIZE // 2, rocket_y + SQUARE_SPEED)
    elif key == GLUT_KEY_DOWN:
        rocket_y = max(ROCKET_SIZE // 2, rocket_y - SQUARE_SPEED)
    elif key == GLUT_KEY_LEFT:
        rocket_x = max(ROCKET_SIZE // 2, rocket_x - SQUARE_SPEED)
    elif key == GLUT_KEY_RIGHT:
        rocket_x = min(WINDOW_WIDTH - ROCKET_SIZE // 2, rocket_x + SQUARE_SPEED)

    glutPostRedisplay()

def init():
    """OpenGL setup er jonno initialization."""
    glClearColor(0.0, 0.0, 0.0, 1.0)  # Background black rakha
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(0, WINDOW_WIDTH, 0, WINDOW_HEIGHT)  # Coordinate system set kore

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

def main():
    """Main function ja OpenGL setup kore ar game loop start kore."""
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
    glutInitWindowSize(WINDOW_WIDTH, WINDOW_HEIGHT)
    glutCreateWindow(b"Rocket Shooting Game")
    
    glutDisplayFunc(display)
    glutKeyboardFunc(keyboard)  # Regular key press handle
    glutSpecialFunc(special_input)  # Special keys (arrow keys) handle
    glutDisplayFunc(display)
    glutTimerFunc(24, update, 0)  # Update loop shuru kore
    init()
    glutMainLoop()

if __name__ == "__main__":
    main()

