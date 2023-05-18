import math

import pyperclip
import time
import pyautogui as autogui
import InputSimulator.InputSimulatorBase as InputSimulatorBase
import Util
from Config import Statics
from Util import GetCurrentTimeStamp, SaveStrToFile
import re

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
GROUP_ANNOUNCEMENT_TOP_LEFT_BUTTON = [334, 228]
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


def PasteGroupName(GroupIndex):
    pyperclip.copy("")
    pyperclip.copy(Statics.GROUP_NAME[GroupIndex])
    InputSimulatorBase.MouseRightClick()
    InputSimulatorBase.MouseMoveToClick(SEARCH_BOX_PASTE_POS, False)


def SelectGroup(GroupIndex):
    OpenWeChat()
    ClickSearchBox()
    PasteGroupName(GroupIndex)
    time.sleep(2)
    InputSimulatorBase.MouseMoveToClick(GROUP_POS, True)


def OpenGroupAnnouncement():
    time.sleep(3)
    InputSimulatorBase.MouseMoveToClick(GROUP_RIGHT_SIDE_BUTTON, True)
    time.sleep(2)
    InputSimulatorBase.MouseMoveToClick(GROUP_ANNOUNCEMENT_EXPAND_BUTTON, True)


def SaveCurrentPaste(Tag):
    Paste = pyperclip.paste()
    if not Paste:
        return False
    LastUpdatedFile = Util.FindLatestUpdatedFile("./Saved/{}".format(Tag))
    SavedPath = "./Saved/{}/{}.txt".format(Tag, GetCurrentTimeStamp())
    SaveStrToFile(Paste, SavedPath)

    if LastUpdatedFile is not False:
        LastUpdatedFileInStr = Util.FileToStr(LastUpdatedFile)
        if FormatString(LastUpdatedFileInStr) == FormatString(Paste):
            Util.Remove(SavedPath)
            return False
    return True


def FormatString(InStr):
    cop = re.compile("[^\u4e00-\u9fa5^a-z^A-Z^0-9]")
    return cop.sub('', InStr)


def SaveGroupAnnouncement(GroupIndex):
    InputSimulatorBase.MouseMoveToClick(GROUP_ANNOUNCEMENT_EDIT_BUTTON, True)
    InputSimulatorBase.MouseMoveToClick(GROUP_ANNOUNCEMENT_TOP_LEFT_BUTTON, True)
    time.sleep(1)
    InputSimulatorBase.SelectAll()
    time.sleep(1)
    InputSimulatorBase.Copy()
    SaveCurrentPaste("Group_Announcement{}".format(GroupIndex))
    InputSimulatorBase.MouseMoveToClick(GROUP_ANNOUNCEMENT_CANCEL_BUTTON, True)


def Reset():
    InputSimulatorBase.MouseMoveToClick(RESET_TAB, True)
    InputSimulatorBase.MouseMoveToClick(PYCHARM_POS, True)


def BackupGroupAnnouncement(GroupIndex):
    SelectGroup(GroupIndex)
    OpenGroupAnnouncement()
    SaveGroupAnnouncement(GroupIndex)
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
    time.sleep(0.2)
    autogui.dragTo(CHAT_MSG_RIGHT_BOTTOM_CORNER[0], CHAT_MSG_RIGHT_BOTTOM_CORNER[1], 1.6, button="left", tween=DragFunc)
    time.sleep(0.2)
    InputSimulatorBase.MouseRelease()
    time.sleep(0.2)
    InputSimulatorBase.Copy()
    time.sleep(0.2)
    InputSimulatorBase.MouseMoveToClick(CHAT_MSG_CANCEL_BUTTON, True)
    time.sleep(0.3)


def SelectAllChatMsg(GroupIndex):
    ScrollToTop()
    ChatMsg = ""
    Count = 0
    for Index in range(50):
        CopyPart()
        IncrementMsg = pyperclip.paste()

        if not IncrementMsg:
            print("Msg has been clear")
            Count = Count + 1
        else:
            if ChatMsg.find(IncrementMsg) != -1:
                # print("\nMatch {} {} [Begin]".format(Count, Util.GetCurrentTimeStamp()))
                # print(IncrementMsg)
                # print("\nMatch [End]\n")

                Count = Count + 1
            else:
                ChatMsg += IncrementMsg
        if Count == 2:
            break
        if Index == 49:
            raise Exception("Try too many times")
    pyperclip.copy(ChatMsg)
    SaveCurrentPaste("Chat_Msg{}".format(GroupIndex))
    return ChatMsg


def GetChatMsg(GroupIndex):
    SelectGroup(GroupIndex)

    ChatMsg = SelectAllChatMsg(GroupIndex)
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
    time.sleep(4)


def EditGroupAnnouncement(Announcement, GroupIndex):
    SelectGroup(GroupIndex)
    OpenGroupAnnouncement()
    EditAnnouncement(Announcement)
    Reset()


def ClearMsg():
    for GroupIndex in range(0, 2):
        SelectGroup(GroupIndex)
        InputSimulatorBase.MouseMoveToClick(GROUP_RIGHT_SIDE_BUTTON, True)
        InputSimulatorBase.MouseMove(CLEAR_AIM_POS, True)
        InputSimulatorBase.MouseScrollDown()
        InputSimulatorBase.MouseMoveToClick(CLEAR_ENTER_POS, True)
        InputSimulatorBase.MouseMoveToClick(CLEAR_CONFIRM_POS, True)
        Reset()
