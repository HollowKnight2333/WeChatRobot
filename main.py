import time, datetime

import pyautogui as autogui
import Util
import pyperclip
import traceback
import Generator.AnnouncementGenerator as Generator
import InputSimulator.ActionSimulator as ActionSimulator
from pynput.mouse import Controller

Mouse = Controller()


def SendConclusionMsg(Begin, End):
    ExcutionTime = (End - Begin) // 1000
    ActionSimulator.SendChatMsg("Good Luck! {}s".format(ExcutionTime))


if __name__ == '__main__':
    bClear = True
    while True:
        CurrentTimeStamp = Util.GetCurrentTimeStamp()
        ZeroAM = int(time.mktime(datetime.date.today().timetuple()))
        NeedClear = False
        # 在0点到9点间休息
        if ZeroAM < CurrentTimeStamp < ZeroAM + 60 * 60 * 9:
            bClear = False
            time.sleep(10 * 60)
        else:
            if not bClear:
                NeedClear = True
                bClear = True
            try:
                ActionSimulator.BackupGroupAnnouncement()
                ChatMsg = ActionSimulator.GetChatMsg()
                GroupAnnouncement = Generator.GenerateAnnouncement(ChatMsg, NeedClear)
                print(GroupAnnouncement)
                pyperclip.copy(GroupAnnouncement)
                if ActionSimulator.SaveCurrentPaste("Group_Announcement"):
                    ActionSimulator.EditGroupAnnouncement(GroupAnnouncement)
                    EndTimeStamp = Util.GetCurrentTimeStamp()
                if ZeroAM < CurrentTimeStamp < ZeroAM + 60 * 60 * 9:
                    time.sleep(60 * 60 * 9)
                else:
                    time.sleep(60 * 5)
            except Exception as e:
                traceback.print_exc()
                ActionSimulator.SendChatMsg("@哈哈呼嘿嘿 exception raised")
                break

    # temp = Util.FileToStr("in.txt")
    # templist = temp.split("\n")
    # out = "["
    # for item in templist:
    #     out += "\"{}\", ".format(item)
    # out += "]"
    # print(out)

    # while True:
    #     print(autogui.position())
    #     time.sleep(0.2)
