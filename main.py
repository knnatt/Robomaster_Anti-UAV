import math
import threading
import numpy as np
import cv2
from mss import mss
from PIL import Image
import pyautogui
import time
from pynput.mouse import Button, Controller

from robot_controller import RobotController

# initial robot.
robot = RobotController()

# initial screen streaming.
screen_size = pyautogui.size()
bounding_box = {'top': 0, 'left': 0, 'width': screen_size.width, 'height': screen_size.height}
print('bounding_box', bounding_box)

sct = mss()

mid_screen_x = screen_size.width / 2
mid_screen_y = screen_size.height / 2
x, y, w, h = None, None, None, None

def detect_red_object(image):
    # Convert the image to HSV color space.
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Create a mask for the red object.

    # lower_color_mask = np.array([0, 50, 50])
    # upper_color_mask = np.array([10, 255, 255])
    lower_color_mask1 = np.array([60, 50, 50])
    upper_color_mask1 = np.array([180, 255, 255])

    mask1 = cv2.inRange(hsv_image, lower_color_mask1, upper_color_mask1)

    lower_color_mask2 = np.array([60, 50, 50])
    upper_color_mask2 = np.array([180, 255, 255])

    mask2 = cv2.inRange(hsv_image, lower_color_mask2, upper_color_mask2)

    # Combine the masks
    mask = cv2.bitwise_or(mask1, mask2)

    # Apply morphological operations to the mask
    # kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    # mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)

    # Find the contours of the red object.
    contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    x, y, largest_contour, w, h = (None, None, None, None, None)

    if(len(contours) > 0):
        # Find the largest contour, which is the red object.
        largest_contour = max(contours, key=cv2.contourArea)

        # # Get the origin point of the red object.
        (x, y, w, h) = cv2.boundingRect(largest_contour)
        mid_x = x + (w / 2)
        mid_y = y + (h / 2)
        # (x, y), radius = cv2.minEnclosingCircle(largest_contour)
    else:
        mid_x, mid_y = None, None

    return (mid_x, mid_y, largest_contour, w, h)

def draw_boundary(image, contour):
    """
    Draws a boundary around the given contour.

    Args:
        image: The image to draw the boundary on.
        contour: The contour to draw the boundary around.
    """

    (x, y, w, h) = cv2.boundingRect(contour)
    cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)

def calculate_relative_position(x1, y1, x2, y2):
    """
    Calculates the relative position of two points.

    Args:
        x1: The x-coordinate of the first point.
        y1: The y-coordinate of the first point.
        x2: The x-coordinate of the second point.
        y2: The y-coordinate of the second point.

    Returns:
        The relative position of the second point to the first point, as a tuple of (x, y).
    """

    x_diff = x2 - x1
    y_diff = y2 - y1
    return (x_diff, y_diff)

def turret_control():
    global x, y, mid_screen_x, mid_screen_y
    print('turret_control start')

    while True:
        _x, _y = x, y
        print('x, y', _x, _y)
        if _x is None or _y is None:
            robot.stop_moving()
            print('stop')
            continue
        else:
            if (mid_screen_x - 50 <= _x <= mid_screen_x + 50) and \
                (mid_screen_y - 50 <= _y <= mid_screen_y + 50):
                robot.stop_moving()
                robot.shoot()
                print('stop')
                continue

            if (mid_screen_x - 250 <= _x <= mid_screen_x + 250) and \
                (mid_screen_y - 250 <= _y <= mid_screen_y + 250):
                if mid_screen_x - 250 <= _x <= mid_screen_x + 250:
                    if _x > mid_screen_x:
                        robot.move_turret_right(slow=True)
                        print('right slow')
                    if _x < mid_screen_x:
                        robot.move_turret_left(slow=True)
                        print('left slow')
                
                if mid_screen_y - 250 <= _y <= mid_screen_y + 250:
                    if _y < mid_screen_y:
                        robot.move_turret_up(slow=True)
                        print('up slow')
                    if _y > mid_screen_y:
                        robot.move_turret_down(slow=True)
                        print('down slow')
                
            else:
                if _y < mid_screen_y:
                    robot.move_turret_up()
                    print('up')
                if _y > mid_screen_y:
                    robot.move_turret_down()
                    print('down')
                if _x > mid_screen_x:
                    robot.move_turret_right()
                    print('right')
                if _x < mid_screen_x:
                    robot.move_turret_left()
                    print('left')

def main():
    global x, y, w, h, mid_screen_y, mid_screen_x

    vid = cv2.VideoCapture(0)
    while True:
        # sct_img = np.array(sct.grab(bounding_box))
        ret, frame = vid.read()
        sct_img = frame
        sct_img = cv2.resize(sct_img, (screen_size.width, screen_size.height), interpolation=cv2.INTER_AREA)
        x, y, contour, w, h = detect_red_object(sct_img)

        # Draw middle cross (x and y axis) line
        cv2.line(sct_img, (0, math.floor(mid_screen_y)), (screen_size.width, math.floor(mid_screen_y)), (0, 0, 0), 3)
        cv2.line(sct_img, (math.floor(mid_screen_x), 0), (math.floor(mid_screen_x), screen_size.height), (0, 0, 0), 3)

        # Draw shoot boundary
        cv2.rectangle(sct_img, 
                      (math.floor(mid_screen_x) - 50, math.floor(mid_screen_y) + 50), 
                      (math.floor(mid_screen_x) + 50, math.floor(mid_screen_y) - 50), 
                      (0, 0, 255), 3)
        
        # Draw slow movement boundary
        cv2.rectangle(sct_img, 
                      (math.floor(mid_screen_x) - 250, math.floor(mid_screen_y) + 250), 
                      (math.floor(mid_screen_x) + 250, math.floor(mid_screen_y) - 250), 
                      (255, 0, 0), 3)

        # Draw robot body move area
        cv2.rectangle(sct_img, 
                      (50, 100), 
                      (screen_size.width - 50, screen_size.height - 100), 
                      (0, 255, 0), 3)

        if (x is not None and y is not None) and (w > 60 and h > 60):
            # In case that robot found object.
            draw_boundary(sct_img, contour)

        else:
            # In case that robot not found object.
            # choose: - re-position of turret (How?)

            # Reset object recognition variables.
            x, y, w, h = None, None, None, None

        cv2.imshow('screen', sct_img)

        if (cv2.waitKey(1) & 0xFF) == ord('q'):
            cv2.destroyAllWindows()
            break

        # time.sleep(0.03)

if __name__ == "__main__":
    # turret_thread = threading.Thread(target=turret_control)
    # turret_thread.start()

    main()
