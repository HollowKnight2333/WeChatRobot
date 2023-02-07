import os
import time
import filecmp


def GetCurrentTimeStamp():
    return int(time.time())


def SaveStrToFile(String, FilePath):
    if String is None:
        return
    file = open(FilePath, 'w+', encoding="utf-8")
    file.write(String)
    file.close()


def IsSame(FileA, FileB):
    if not os.path.exists(FileA) or not os.path.exists(FileB):
        return False
    return filecmp.cmp(FileA, FileB)


def FindLatestUpdatedFile(FilePath):
    List = os.listdir(FilePath)
    if not List:
        return False
    List.sort(key=lambda fn: os.path.getmtime(FilePath + "/" + fn))
    return os.path.join(FilePath, List[-1])


def Remove(Path):
    if os.path.exists(Path):
        os.remove(Path)


def FileToStr(Path):
    if not os.path.exists(Path):
        return

    return open(Path, encoding="utf-8").read()


def FormatTimeToTimeStamp(FormatTime):
    TimeArray = time.strptime(FormatTime, "%Y-%m-%d %H:%M:%S")
    return int(time.mktime(TimeArray))


def GetLCSLength(s1, s2):
    m = [[0 for i in range(len(s2) + 1)] for j in range(len(s1) + 1)]
    mmax = 0  # 最长匹配的长度
    p = 0  # 最长匹配对应在s1中的最后一位
    for i in range(len(s1)):
        for j in range(len(s2)):
            if s1[i] == s2[j]:
                m[i + 1][j + 1] = m[i][j] + 1
                if m[i + 1][j + 1] > mmax:
                    mmax = m[i + 1][j + 1]
                    p = i + 1
    return mmax  # 返回最长子串其长度
