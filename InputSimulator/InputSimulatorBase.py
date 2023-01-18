import time
import pynput.keyboard as keyboard
import pynput.mouse as mouse
import pyautogui as autogui

Keyboard = keyboard.Controller()
Key = keyboard.Key

Mouse = mouse.Controller()
Button = mouse.Button

MOUSE_MOVE_DURATION = 0.2
INPUT_OPERATION_GAP = 0.1


def MousePress():
    autogui.mouseDown()
    time.sleep(INPUT_OPERATION_GAP)


def MouseRelease():
    autogui.mouseUp()
    time.sleep(INPUT_OPERATION_GAP)


def MouseRollBack():
    autogui.scroll(5)
    time.sleep(0.2)


def MouseScrollUp():
    autogui.scroll(1000)
    time.sleep(0.2)


def MouseScrollDown():
    autogui.scroll(-1000)
    time.sleep(0.2)


def MouseMove(TargetPos, Absolute):
    PosX = TargetPos[0]
    PosY = TargetPos[1]
    autogui.moveTo(PosX, PosY, duration=MOUSE_MOVE_DURATION)
    time.sleep(INPUT_OPERATION_GAP)


def MouseClick():
    Pos = autogui.position()
    autogui.click(Pos.x, Pos.y, button="left")
    time.sleep(INPUT_OPERATION_GAP)


def MouseRightClick():
    Pos = autogui.position()
    autogui.click(Pos.x, Pos.y, button="right")
    time.sleep(INPUT_OPERATION_GAP)


def MouseMoveToClick(TargetPos, Absolute):
    MouseMove(TargetPos, Absolute)
    MouseClick()


def SelectAll():
    autogui.hotkey('command', 'a')
    time.sleep(INPUT_OPERATION_GAP)


def Copy():
    autogui.hotkey('command', 'c')
    time.sleep(INPUT_OPERATION_GAP)


def Paste():
    autogui.hotkey('command', 'v')
    time.sleep(INPUT_OPERATION_GAP)


def PressEnter():
    autogui.press('enter')
    time.sleep(INPUT_OPERATION_GAP)


def PressDelete():
    autogui.press('delete')
    time.sleep(INPUT_OPERATION_GAP)
