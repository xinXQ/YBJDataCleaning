# -*- coding:utf-8 -*-
"""
根据文件夹路径,找到所有的符合要求的文件
"""
import os


class TargetFile:
    def __init__(self, fp, errp=None):
        self.filePath = fp
        self.errPath = errp

    def getFp(self):
        return self.filePath

    def getErrp(self):
        return self.errPath


def classifyFiles(path, filter, l=None):
    # path: 目录
    # filter: 过滤函数,返回bool
    # l: 结果集
    # 返回一个list, 包含符合要求的所有文件完整路径名
    if l is None:
        l = []
    abspath = os.path.abspath(path)
    iterms = os.listdir(abspath)
    for iterm in iterms:
        p = os.path.join(abspath, iterm)
        if os.path.isdir(p):
            classifyFiles(p, filter, l)
        elif filter(p):
            l.append(p)
    return l


class FileUtil:
    """
    这个class 是为了方便操作文件的, 写文件, 查找文件标志是否存在
    @defaultPath: 要操作的根目录

    getWriteFilePath: 这个返回一个对象, 包括异常和正常的文件输出全路径,会自动创建父目录
    getlatestFile: 获取根目录下, 同一文件名字的最新的文件
    checkExitTag: 查看根目录下,标志是否存在
    """
    def __init__(self, defaultPath='E:/pyworkspaces/YBJ/mid/'):
        self.path = defaultPath

    def _get_dir_path(self, tag):
        DIRPARENT = self.path
        if not os.path.exists(DIRPARENT):
            os.mkdir(DIRPARENT)
        lsdir = os.listdir(DIRPARENT)
        i = self.checkExitTag(tag)
        tagd = lsdir[i - 1] + "/" if i > 0 else str(len(lsdir)).zfill(4) + "-tag" + "/"
        dirPath = DIRPARENT + tagd.replace('tag', tag)
        if not os.path.exists(dirPath):
            os.mkdir(dirPath)
        return dirPath

    def getWriteFilePath(self, ph, tag, others=None):
        # print(ph)
        targetDir = self._get_dir_path(tag)
        lps = os.path.split(ph)
        dirp = targetDir + os.path.split(lps[0])[1]
        fileName = dirp + '/' + lps[1]
        if others is not None:
            others = dirp + '/' + others
        os.makedirs(dirp, exist_ok=True)
        return TargetFile(fileName, others)

    def getlatestFile(self, fn):
        DIRPARENT = self.path
        l = classifyFiles(DIRPARENT, lambda x: x.endswith(fn))
        l.sort()
        return l[-1]

    def checkExitTag(self, tag):
        DIRPARENT = self.path
        lsdir = os.listdir(DIRPARENT)
        i = len(lsdir)
        while i and not lsdir[i - 1].__contains__(tag):
            i -= 1
        return i


def writeLine(fw, ls, flag=True):
    if flag:
        fw.writelines(ls)
        fw.flush()
    else:
        fw.writelines(ls)
        fw.close()
    ls.clear()


if __name__ == '__main__':
    testp = "E:\\pyworkspaces\\YBJ\\srcdata\\340400-淮南"
    # l = classifyFiles("E:\pyworkspaces\YBJ\srcdata\\", lambda x: x.endswith("xx.txt"))
    # for i in l:
    #     d = getWriteFilePath(i, "a6", "idcheck_err")
    #     open(d.filePath, 'a')
    #     if d.errPath is not None:
    #         open(d.errPath, 'a')
    #     print(d.filePath, d.errPath)
    # latestFile = getlatestFile("340722_rycbxx.txt")
    # print(latestFile)
