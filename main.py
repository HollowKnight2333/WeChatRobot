import time, datetime

import pyautogui as autogui
import Util
import pyperclip
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
        else:
            if not bClear:
                NeedClear = True
                bClear = True
            try:
                for GroupIndex in range(0, 2):
                    ActionSimulator.BackupGroupAnnouncement(GroupIndex)

                ChatMsg0 = ActionSimulator.GetChatMsg(0)
                ChatMsg1 = ActionSimulator.GetChatMsg(1)
                GroupAnnouncement = Generator.GenerateAnnouncement(ChatMsg0, ChatMsg1, NeedClear)
                print(GroupAnnouncement)
                pyperclip.copy(GroupAnnouncement)
                for GroupIndex in range(0, 2):
                    if ActionSimulator.SaveCurrentPaste("Group_Announcement{}".format(GroupIndex)):
                        ActionSimulator.EditGroupAnnouncement(GroupAnnouncement, GroupIndex)
                        EndTimeStamp = Util.GetCurrentTimeStamp()
                if ZeroAM < CurrentTimeStamp < ZeroAM + 60 * 60 * 9:
                    time.sleep(60 * 60 * 9)
                else:
                    time.sleep(60 * 60 * 2)
            except Exception as e:
                print(e)
                ActionSimulator.SendChatMsg("@呼呼哈嘿嘿 exception raised")
                break
    # while True:
    #     print(autogui.position())
    #     time.sleep(0.2)
