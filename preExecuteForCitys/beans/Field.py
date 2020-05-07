# _*_ coding=utf-8 _*_

"""
表示一个字段 名称, 状态, 检测逻辑, 信息
"""


class Field:
    def __init__(self, name, value, stat=True, info=""):
        assert isinstance(name, str)
        assert isinstance(stat, bool)
        assert isinstance(info, str)
        self.name = name
        self.value = value
        self.stat = stat
        self.info = info

    def __str__(self):
        return "{}: {}, stat: {}, info: {}".format(self.name, self.value, self.stat, self.info)

    __repr__ = __str__
