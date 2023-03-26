import re
import time
import jionlp
import Util
import InputSimulator.ActionSimulator as ActionSimulator
import Config.Statics as Config

DefaultTag = "吃喝玩乐"
TagList = ["吴彦祖/刘亦菲", "剧本杀", "密室", "音乐Live", "户外/运动", "出游", "境外旅游", DefaultTag]
CharmingList = []
Activities = {}
HasBeenHandled = {}
ActivitiesWithTag = {}
ValidChatMsg = {}
ChatMsgs = []

MAX_COUNT = 30


def Clear():
    global Activities, ActivitiesWithTag, ValidChatMsg, ChatMsgs
    Activities = {}
    ActivitiesWithTag = {}
    ValidChatMsg = {}
    ChatMsgs = []
    for Tag in TagList:
        ActivitiesWithTag.update({Tag: []})


def GetNumOfActivitiesFromSender(SenderName):
    global Activities
    List = Activities.get(SenderName)
    if not List:
        return 0
    return len(List)


def CheckEnableAdd(SenderName, TimeConfig):
    ActivityTimeStamp = Util.FormatTimeToTimeStamp(TimeConfig["time"][0])
    if Util.GetCurrentTimeStamp() > ActivityTimeStamp:
        return False
    return True


def IsCharming(SenderName):
    for Charming in CharmingList:
        if SenderName == Charming:
            return True
    return False


def IsChamberTag(SendContent):
    if SendContent.find("密室") != -1:
        return True
    return False


def IsLARP(SendContent):
    if SendContent.find("《") != -1:
        return True

    List = SendContent.split(" ")
    for Str in List:
        if re.search(".+本", Str) is not None:
            return True
    return False


def IsTravelAbroad(SendContent, TimeConfig):
    if CheckExists(SendContent, Config.CountryList) or CheckExists(SendContent, Config.CityAbroadList):
        return True
    return False


def IsTravel(SendContent, TimeConfig):
    if CheckExists(SendContent, Config.TravelList):
        return True
    return False


def IsSport(SendContent):
    if CheckExists(SendContent, Config.SportList) or CheckExists(SendContent, Config.MountainList):
        return True
    return False


def CheckExists(Content, List):
    for Item in List:
        if Content.find(Item) != -1:
            return True
    return False


def IsLive(SendContent):
    if CheckExists(SendContent, Config.LiveList):
        return True
    return False


def GetTag(SendContent, SenderName, TimeConfig):
    if IsCharming(SenderName):
        return "吴彦祖/刘亦菲"

    if IsChamberTag(SendContent):
        return "密室"

    if IsLARP(SendContent):
        return "剧本杀"

    if IsLive(SendContent):
        return "音乐Live"

    if IsSport(SendContent):
        return "户外/运动"

    if IsTravelAbroad(SendContent, TimeConfig):
        return "境外旅游"

    if IsTravel(SendContent, TimeConfig):
        return "出游"

    return DefaultTag


def SplitRequirement(SendContent):
    return SendContent, ""


def AddActivity(SenderName, SendContent, TimeConfig, ChatMsg):
    if not CheckEnableAdd(SenderName, TimeConfig):
        return

    global Activities, ActivitiesWithTag
    if not Activities.get(SenderName):
        Activities.update({SenderName: []})

    SendContent, Requirement = SplitRequirement(SendContent)
    Tag = GetTag(SendContent, SenderName, TimeConfig)

    Activity = {
        "SenderName": SenderName,
        "SendContent": SendContent,
        "Tag": GetTag(SendContent, SenderName, TimeConfig),
        "TimeStamp": Util.FormatTimeToTimeStamp(TimeConfig["time"][0]),
        "Requirement": Requirement,
        "TimeConfig": TimeConfig,
        "ChatMsg": ChatMsg,
    }

    Activities[SenderName].append(Activity)
    ActivitiesWithTag[Tag].append(Activity)


def DateFormat(SendContent, Symbol, SplitSymbol):
    # AllList = re.findall("(1[0-2]|[1-9]){}([1-9]|([1-3][0-9]))".format(Symbol), SendContent)
    # for Match in AllList:
    #     Split = Match.split(SplitSymbol)
    #     SendContent = SendContent.replace(Match[:-1], "{}月{}日 ".format(Split[0], Split[1][:-1]))
    #
    # AllList = re.findall("(?:1[0-2]|[1-9]){}([1-9]|([1-3][0-9]))".format(Symbol), SendContent)
    # for Match in AllList:
    #     Split = Match.split(SplitSymbol)
    #     SendContent = SendContent.replace(Match[:-1], "{}月{}日 ".format(Split[0], Split[1][:-1]))

    return SendContent


def FormatDateMatch(SendContent, Symbol):
    List = SendContent.split(" ")
    for Segment in List:
        Temp = Segment.split(Symbol)
        if len(Temp) != 2:
            continue
        CandidateMonth = Temp[0]
        if not re.fullmatch("^(0?[1-9]|1[0-2])$", CandidateMonth):
            continue
        CandidateDay = Temp[1]
        Len = 2
        if len(CandidateDay) > 2:
            CandidateDay = CandidateDay[:2]
            Len = 2
        if not re.fullmatch("[0-3][0-9]", CandidateDay):
            CandidateDay = CandidateDay[:1]
            Len = 1
            if not re.fullmatch("[1-9]", CandidateDay):
                continue
        Part = Temp[0] + Symbol + Temp[1][:Len]
        SendContent = SendContent.replace(Part, "{}月{}日".format(CandidateMonth, CandidateDay))
    return SendContent


def FormatSendContent(SendContent):
    SendContent = SendContent[5:]
    SendContent = SendContent.replace("，", " ")
    SendContent = SendContent.replace(",", " ")
    OriginSendContent = SendContent
    Output = FormatDateMatch(SendContent, "月")
    Output = FormatDateMatch(SendContent, ".")
    return Output, OriginSendContent


def ActivityToString(Activity, Count):
    # TimeDesc = ""
    # TimeConfig = Activity["TimeConfig"]
    # TimeType = TimeConfig["type"]
    # if TimeType == "time_point":
    #     TimeStamp = TimeConfig["time"][0]
    #     TimeStamp = Util.FormatTimeToTimeStamp(TimeStamp)
    #     TimeDesc = time.strftime("%m-%d %H:%M", time.localtime(TimeStamp))
    SenderName = Activity["SenderName"]
    SendContent = Activity["SendContent"]
    Requirement = Activity["Requirement"]
    Desc = SendContent + Requirement
    Desc = Desc.rstrip()
    return "【{}】 {}, 上车滴滴:{}。\n".format(Count, Desc, SenderName)


def Delete(SenderName, Param):
    global Activities, ActivitiesWithTag
    List = Activities.get(SenderName)
    if not List or len(List) == 0:
        return

    TargetIndex = 0
    TargetContent = List[0]["SendContent"]
    if Param is not None:
        LCS = Util.GetLCSLength(TargetContent, Param)
        for i in range(1, len(List)):
            Activity = List[i]
            Content = Activity["SendContent"]
            CurrentLCS = Util.GetLCSLength(Content, Param)
            if CurrentLCS > LCS:
                TargetIndex = i
                LCS = CurrentLCS
                TargetContent = Content

    del Activities.get(SenderName)[TargetIndex]

    for key in ActivitiesWithTag.keys():
        List = ActivitiesWithTag[key]
        Index = 0
        for Activity in List:
            if Activity["SendContent"] == TargetContent:
                del ActivitiesWithTag[key][Index]
                return
            Index += 1


def ExecuteCommand(SenderName, SendContent):
    List = SendContent.split(" ")
    if len(List) == 0:
        return False
    Command = List[0]
    if Command == "-d":
        if len(List) > 1:
            Delete(SenderName, List[1])
        else:
            Delete(SenderName, None)
        return True
    return False


def GetSenderName(ChatMsg):
    FindStr = re.findall(".+ [0-9]{4}/[0-9]{2}/[0-9]{2}", ChatMsg)
    return FindStr[0][:-11]


def Preprocess(ChatMsg):
    return ChatMsg.replace("本周", "这周")


def GenerateAnnouncement(ChatMsg, bClearMsg):
    global ValidChatMsg, ChatMsgs, HasBeenHandled
    Clear()
    ChatMsg = Util.FileToStr("./Saved/Filtered_Chat_Msg/ChatMsg.txt") + ChatMsg
    ChatMsg = ChatMsg.replace("\r", "\n")
    FindLists = re.findall(".+[0-9]{2}.+[0-9]{2}\n@Bot[\s\S]*?\n\n", ChatMsg)
    HasBeenHandled = {}
    for ChatMsg in FindLists:
        ChatMsg = Preprocess(ChatMsg)
        if HasBeenHandled.get(ChatMsg):
            continue
        HasBeenHandled.update({ChatMsg: True})

        ChatMsgs.append(ChatMsg)
        ChatMsgSplit = ChatMsg.split("\n")
        if len(ChatMsgSplit) < 4:
            continue
        SenderName = GetSenderName(ChatMsg)
        SendContent = ""
        for i in range(1, len(ChatMsgSplit)):
            if ChatMsgSplit[i] != "":
                SendContent += ChatMsgSplit[i]
                if i != len(ChatMsgSplit) - 1:
                    SendContent += " "

        SendContent, OriginSendContent = FormatSendContent(SendContent)
        if ExecuteCommand(SenderName, OriginSendContent):
            continue
        try:
            TimeConfig = jionlp.parse_time(SendContent, time_base=time.time())
            if TimeConfig["time"] and len(TimeConfig["time"]) > 0:
                AddActivity(SenderName, OriginSendContent, TimeConfig, ChatMsg)
        except:
            print("Exception Raised:", OriginSendContent)

    Count = 0
    TagCount = 0
    Announcement = ""
    for Tag in TagList:
        ActivityList = ActivitiesWithTag[Tag]
        if Count == MAX_COUNT:
            break
        if len(ActivityList) == 0:
            continue
        if TagCount == 0:
            Announcement += "★{}★\n".format(Tag)
        else:
            Announcement += "\n★{}★\n".format(Tag)
        TagCount += 1
        SortList = sorted(ActivityList, key=lambda d: d['TimeStamp'])
        Cnt = 0
        for Activity in SortList:
            Cnt += 1
            Announcement += ActivityToString(Activity, Cnt)
            Count += 1
            if Count > MAX_COUNT:
                break
        # Announcement += "\n"
    Announcement += Util.FileToStr("./Config/std.txt")

    if bClearMsg:
        for Tag in TagList:
            ActivityList = ActivitiesWithTag[Tag]
            if len(ActivityList) == 0:
                continue
            for Activity in ActivityList:
                ValidChatMsg.update({Activity["ChatMsg"]: True})
        Filtered_Chat_Msg = ""
        for ChatMsg in ChatMsgs:
            if ValidChatMsg.get(ChatMsg):
                Filtered_Chat_Msg += ChatMsg

        Util.SaveStrToFile(Filtered_Chat_Msg, "./Saved/Filtered_Chat_Msg/ChatMsg.txt")
        ActionSimulator.ClearMsg()

    return Announcement
