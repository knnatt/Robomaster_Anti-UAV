import pyautogui
from time import sleep

DELAY = 0.001

class RobotController:
    def __init__(self):
        pass

    def forward(self):
        pyautogui.keyDown('w')
        # sleep(DELAY)
        # pyautogui.keyUp('w')
    
    def backward(self):
        pyautogui.keyDown('s')
        # sleep(DELAY)
        # pyautogui.keyUp('s')

    def left(self):
        pyautogui.keyDown('a')
        # sleep(DELAY)
        # pyautogui.keyUp('a')

    def right(self):
        pyautogui.keyDown('d')
        # sleep(DELAY)
        # pyautogui.keyUp('d')

    def move_turret_up(self, slow: bool = False):
        if slow:
            pyautogui.press('up')
        else:
            pyautogui.keyDown('up')
            sleep(DELAY)
            pyautogui.keyUp('up')

    def move_turret_down(self, slow: bool = False):
        if slow:
            pyautogui.press('down')
        else:
            pyautogui.keyDown('down')
            sleep(DELAY)
            pyautogui.keyUp('down')
    
    def move_turret_left(self, slow: bool = False):
        if slow:
            pyautogui.press('left')
        else:
            pyautogui.keyDown('left')
            sleep(DELAY)
            pyautogui.keyUp('left')
    
    def move_turret_right(self, slow: bool = False):
        if slow:
            pyautogui.press('right')
        else:
            pyautogui.keyDown('right')
            sleep(DELAY)
            pyautogui.keyUp('right')

    def stop_moving(self):
        # pass
        # pyautogui.keyUp('w')
        # pyautogui.keyUp('a')
        # pyautogui.keyUp('s')
        # pyautogui.keyUp('d')
        pyautogui.keyUp('up')
        pyautogui.keyUp('down')
        pyautogui.keyUp('left')
        pyautogui.keyUp('right')
        sleep(DELAY)

    def shoot(self):
        pyautogui.click()
