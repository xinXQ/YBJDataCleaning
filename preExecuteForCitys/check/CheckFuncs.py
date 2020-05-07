# _*_ coding=utf-8 _*_
import re
from datetime import date

from preExecuteForCitys.beans.Field import Field
from preExecuteForCitys.utils.DictParse import DictParse
from preExecuteForCitys.utils.IDCheck import IDCheck

pd = DictParse()
res = pd.areaMatching()
assert isinstance(res, dict)


# 检测是不是空
def checkIsNone(field):
    assert isinstance(field, Field)
    stat = field.value is not None and "" != field.value
    info = field.name + ":非空检测失败" if not stat else ""
    field.stat = stat
    field.info += info
    return stat


# 检测在不在字典表
def checkInDic(field):
    assert isinstance(field, Field)
    if field.name not in pd.parseData.keys():
        print("字典表检测失败, 所查 {} 不在,字典表类型中".format(field.name))
        raise Exception("字典表检测失败, 所查 {} 不在,字典表类型中".format(field.name))
    vs = pd.parseData[field.name]
    stat = True if field.value in vs else False
    info = "{}:{} 字典表检测失败".format(field.name, field.value) if not stat else ""
    field.stat = stat
    field.info += info
    return stat


# 检测身份证
def checkIdVali(field):
    assert isinstance(field, Field)
    if field.name != "CERT_NO":
        raise Exception("不是证件号码不可以做这个检验")
    stat = isIdCard(field.value)
    info = field.value + ":身份证检测失败" if not stat else ""
    field.stat = stat
    field.info += info
    return stat


# 检测生日
def checkDate(field):
    assert isinstance(field, Field)
    dt = field.value
    try:
        d = date(int(dt[:4]), int(dt[4:6]), int(dt[6:8]))
        stat = False if d < date(1870, int('01'), int('01')) else True
    except ValueError:
        stat = False
    info = field.value + ": 生日检测失败" if not stat else ""
    field.stat = stat
    field.info += info
    return stat


# 检查是否数字加大写字母
def checkId(field):
    assert isinstance(field, Field)
    stat = True
    for _char in field.value:
        if u'\u0041' <= _char <= u'\u005a':
            continue
        if u'\u0030' <= _char <= u'\u0039':
            continue
        stat = False
    info = field.value + ": id存在非法字符" if not stat else ""
    field.stat = stat
    field.info += info
    return stat


# 字符是否是中文, 引文, 空格, 间隔号
def checkChar(field):
    assert isinstance(field, Field)
    if field.name != "NAME":
        raise Exception("不是姓名不可以做这个检验")
    stat = True
    for _char in field.value:
        # 英文
        if (u'\u0041' <= _char <= u'\u005a') or (u'\u0061' <= _char <= u'\u007a'):
            continue
        # 中文
        if '\u4e00' <= _char <= '\u9fa5':
            continue
        # 空格
        if _char in ['\u00A0', '\u0020', '\u3000']:
            continue
        # 间隔
        if _char in ['\uFF0E', '\u00B7']:
            continue
        stat = False
    info = field.value + ": Name存在非法字符" if not stat else ""
    field.stat = stat
    field.info += info
    return stat


# 身份证合法性检验
def isIdCard(field):
    assert isinstance(field, Field)
    id_card = field.value
    cls = IDCheck
    stat = True
    info = ""
    if len(id_card) != 18:
        stat = False
        info = "身份证18位检验失败"
    elif not re.match(r"^\d{17}(\d|X)$", id_card):
        stat = False
        info = "身份证格式检验失败"
    elif not cls.is_date(id_card):
        stat = False
        info = "身份证时间检验失败"
    elif str(cls.get_id_card_verify_number(id_card)) != str(id_card.upper()[-1]):
        stat = False
        info = "身份证校验位检验失败"
    field.stat = stat
    field.info += info
    return stat


# 验证参保状态变更原因
def checkcisrea(field):
    assert isinstance(field, Field)
    if field.name == "CIS_REA" and field.value == "":
        field.stat = True
        return True
    stat = checkInDic(field)
    info = "" if stat else "{}:参保状态变更字段不在字典表".format(field.value)
    field.stat = stat
    field.info += info
    return stat


# 检查日期合法性
def checkDateVail(field):
    assert isinstance(field, Field)
    if field.value is None or "" == field.value:
        field.stat = False
        field.info += "开始时间为空"
        return False
    try:
        date(int(field.value[:4]), int(field.value[4:6]), 1)
        field.stat = True
        return True
    except Exception:
        field.stat = False
        field.info += "{}:开始时间为非法格式".format(field.value)
        return False


def checkDateVailEm(field):
    assert isinstance(field, Field)
    if field.value is None or "" == field.value:
        field.stat = True
        return True
    try:
        date(int(field.value[:4]), int(field.value[4:6]), 1)
        field.stat = True
        return True
    except Exception:
        field.stat = False
        field.info += "{}:截至时间时间为非法格式".format(field.value)
        return False


if __name__ == '__main__':
    # print(checkDate(Field("", "18690101")))
    st = "朱六－"
    print(checkChar(Field("NAME", st)))
    print('－'.encode('unicode_escape').decode())
    print(''.encode('unicode_escape').decode())
    # print("-", '\uFF0E', '\u002E', "-")
    st = "23RRw89"
    print(checkId(Field("", st)))
