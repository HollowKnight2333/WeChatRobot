import math

import pyperclip
import time
import pyautogui as autogui
import InputSimulator.InputSimulatorBase as InputSimulatorBase
import Util
from Config import Statics
from Util import GetCurrentTimeStamp, SaveStrToFile

WECHAT_APP_POS = [1164, 1064]
PYCHARM_POS = [1237, 1079]

SEARCH_BOX_POS = [124, 58]
SEARCH_BOX_PASTE_POS = [184, 112]

GROUP_POS = [200, 133]
GROUP_RIGHT_SIDE_BUTTON = [950, 56]
# 群成员人数不同，位置不同
GROUP_ANNOUNCEMENT_EXPAND_BUTTON = [752, 523]  # 大群
# GROUP_ANNOUNCEMENT_EXPAND_BUTTON = [1249, 526]  # 测试群
GROUP_ANNOUNCEMENT_EDIT_BUTTON = [461, 593]
GROUP_ANNOUNCEMENT_TOP_LEFT_BUTTON = [318, 232]
GROUP_ANNOUNCEMENT_CANCEL_BUTTON = [424, 593]

GROUP_ANNOUNCEMENT_CONFIRM_BUTTON = [559, 599]
GROUP_ANNOUNCEMENT_SUBMIT_BUTTON = [543, 438]

CHAT_MSG_RIGHT_BOTTOM_CORNER = [979, 984]
CHAT_MSG_TOP_LEFT_CORNER = [330, 95]
CHAT_MSG_CANCEL_BUTTON = [927, 650]

INPUT_TEXT_REGION = [344, 638]
SEND_BUTTON = [1064, 635]

RESET_TAB = [198, 327]
SCROLL_TIMES = 80

CLEAR_AIM_POS = [830, 452]
CLEAR_ENTER_POS = [842, 671]
CLEAR_CONFIRM_POS = [562, 414]


def OpenWeChat():
    InputSimulatorBase.MouseMoveToClick(WECHAT_APP_POS, True)


# Suppose that WeChat is opened
def ClickSearchBox():
    InputSimulatorBase.MouseMoveToClick(SEARCH_BOX_POS, True)


def PasteGroupName():
    pyperclip.copy("")
    pyperclip.copy(Statics.GROUP_NAME)
    InputSimulatorBase.MouseRightClick()
    InputSimulatorBase.MouseMoveToClick(SEARCH_BOX_PASTE_POS, False)


def SelectGroup():
    OpenWeChat()
    ClickSearchBox()
    PasteGroupName()
    time.sleep(2)
    InputSimulatorBase.MouseMoveToClick(GROUP_POS, True)


def OpenGroupAnnouncement():
    time.sleep(3)
    InputSimulatorBase.MouseMoveToClick(GROUP_RIGHT_SIDE_BUTTON, True)
    time.sleep(2)
    InputSimulatorBase.MouseMoveToClick(GROUP_ANNOUNCEMENT_EXPAND_BUTTON, True)


def SaveCurrentPaste(Tag):
    Paste = pyperclip.paste()
    LastUpdatedFile = Util.FindLatestUpdatedFile("./Saved/{}".format(Tag))
    SavedPath = "./Saved/{}/{}.txt".format(Tag, GetCurrentTimeStamp())
    SaveStrToFile(Paste, SavedPath)

    if LastUpdatedFile is not False and Util.IsSame(LastUpdatedFile, SavedPath):
        Util.Remove(SavedPath)
        return False
    return True


def SaveGroupAnnouncement():
    InputSimulatorBase.MouseMoveToClick(GROUP_ANNOUNCEMENT_EDIT_BUTTON, True)
    InputSimulatorBase.MouseMoveToClick(GROUP_ANNOUNCEMENT_TOP_LEFT_BUTTON, True)
    time.sleep(0.5)
    InputSimulatorBase.SelectAll()
    time.sleep(0.5)
    InputSimulatorBase.Copy()
    SaveCurrentPaste("Group_Announcement")
    InputSimulatorBase.MouseMoveToClick(GROUP_ANNOUNCEMENT_CANCEL_BUTTON, True)


def Reset():
    InputSimulatorBase.MouseMoveToClick(RESET_TAB, True)
    InputSimulatorBase.MouseMoveToClick(PYCHARM_POS, True)


def BackupGroupAnnouncement():
    SelectGroup()
    OpenGroupAnnouncement()
    SaveGroupAnnouncement()
    Reset()


def ScrollToTop():
    InputSimulatorBase.MouseMoveToClick(CHAT_MSG_TOP_LEFT_CORNER, True)
    for Index in range(SCROLL_TIMES):
        InputSimulatorBase.MouseScrollUp()


def DragFunc(n):
    return 1 - math.pow(1 - n, 5)


def CopyPart():
    InputSimulatorBase.MouseMoveToClick(CHAT_MSG_TOP_LEFT_CORNER, True)
    time.sleep(0.5)
    InputSimulatorBase.MousePress()
    time.sleep(0.5)
    autogui.dragTo(950, 231, 3, button="left", mouseDownUp=False)
    autogui.dragTo(CHAT_MSG_RIGHT_BOTTOM_CORNER[0], CHAT_MSG_RIGHT_BOTTOM_CORNER[1], 3, button="left", tween=DragFunc)
    InputSimulatorBase.MouseRelease()
    InputSimulatorBase.Copy()
    time.sleep(0.2)
    InputSimulatorBase.MouseMoveToClick(CHAT_MSG_CANCEL_BUTTON, True)
    time.sleep(0.3)


def SelectAllChatMsg():
    ScrollToTop()
    ChatMsg = ""
    Count = 0
    for Index in range(40):
        CopyPart()
        IncrementMsg = pyperclip.paste()
        if not IncrementMsg or ChatMsg.find(IncrementMsg) != -1:
            break
        ChatMsg += IncrementMsg
    pyperclip.copy(ChatMsg)
    SaveCurrentPaste("Chat_Msg")
    return ChatMsg


def GetChatMsg():
    SelectGroup()

    ChatMsg = SelectAllChatMsg()
    Reset()

    return ChatMsg


def SendChatMsg(ChatMsg):
    SelectGroup()
    InputSimulatorBase.MouseMoveToClick(INPUT_TEXT_REGION, True)
    pyperclip.copy(ChatMsg)
    InputSimulatorBase.Paste()
    InputSimulatorBase.PressEnter()
    Reset()


def EditAnnouncement(Announcement):
    InputSimulatorBase.MouseMoveToClick(GROUP_ANNOUNCEMENT_EDIT_BUTTON, True)
    InputSimulatorBase.MouseMoveToClick(GROUP_ANNOUNCEMENT_TOP_LEFT_BUTTON, True)
    time.sleep(0.5)
    InputSimulatorBase.SelectAll()
    time.sleep(0.5)
    InputSimulatorBase.PressDelete()
    pyperclip.copy(Announcement)
    InputSimulatorBase.Paste()
    InputSimulatorBase.MouseMoveToClick(GROUP_ANNOUNCEMENT_TOP_LEFT_BUTTON, True)
    InputSimulatorBase.MouseMoveToClick(GROUP_ANNOUNCEMENT_CONFIRM_BUTTON, True)
    InputSimulatorBase.MouseMoveToClick(GROUP_ANNOUNCEMENT_SUBMIT_BUTTON, True)


def EditGroupAnnouncement(Announcement):
    SelectGroup()
    OpenGroupAnnouncement()
    EditAnnouncement(Announcement)
    Reset()


def ClearMsg():
    SelectGroup()
    InputSimulatorBase.MouseMoveToClick(GROUP_RIGHT_SIDE_BUTTON, True)
    InputSimulatorBase.MouseMove(CLEAR_AIM_POS, True)
    InputSimulatorBase.MouseScrollDown()
    InputSimulatorBase.MouseMoveToClick(CLEAR_ENTER_POS, True)
    InputSimulatorBase.MouseMoveToClick(CLEAR_CONFIRM_POS, True)
    Reset()
