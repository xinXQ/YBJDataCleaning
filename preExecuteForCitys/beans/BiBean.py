# _*_ coding=utf-8 _*_

"""
这是 基础信息 数据的bean
POOLAREA,PSN_NO,NAME,GEND,CERT_TYPE,CERT_NO,BRDY,NATY,NAT_REGN_CODE,SURV_STAS
医保区划编码,人员编号,姓名,性别,证件类型,证件号码,出生日期,民族,国家和地区代码,生存状态
"""
import time

from preExecuteForCitys.beans.Field import Field
from preExecuteForCitys.check.CheckFuncs import isIdCard, checkId
from preExecuteForCitys.utils.CheckByFieldName import biRole


class BiBeanFieldsLenErr(Exception):
    pass


class BiBean:
    _fields = ["POOLAREA", "PSN_NO", "NAME", "GEND", "CERT_TYPE",
               "CERT_NO", "BRDY", "NATY", "NAT_REGN_CODE", "SURV_STAS"]

    def __init__(self, fields):
        if len(fields) != len(self._fields):
            raise BiBeanFieldsLenErr("基础信息数据字段不是10位")
        self._info = []
        self.fileds = {self._fields[x]: Field(self._fields[x], fields[x]) for x in range(len(self._fields))}

    def __str__(self):
        return "\n".join([str(f) for f in self.fileds.values()])

    __repr__ = __str__

    # 获取这个bean的最终结果
    def check(self):
        allFiledsStat = self.checkAllFields()
        revleCheckStat = self.relevanceCheck()
        if not revleCheckStat:
            self._info.append("证件类型和证件号码检验异常")
        self._info.extend([f.info for f in self.fileds.values()])
        self._info = [x for x in self._info if x != ""]
        return allFiledsStat and revleCheckStat

    # 基础信息表的内部关联检查 !!
    def relevanceCheck(self):
        ct = self.fileds["CERT_TYPE"]
        cn = self.fileds["CERT_NO"]
        assert isinstance(ct, Field)
        assert isinstance(cn, Field)
        # 1,当证件类型为居民身份证（户口簿）时，证件号码必须为18位,并且必须符合身份证校验规则，包括性别、出生日期和校验位。
        # 2,当证件号码为合法身份证时，证件类型必须为居民身份证（户口簿）。
        a = isIdCard(cn)
        f1 = "01" == ct.value if a else False
        f2 = a if "01" == ct.value else cn.stat
        return f1 and f2

    # 将每个field根据规范进行检查
    def checkAllFields(self):
        for k, v in self.fileds.items():
            res = [r(v) for r in biRole[k]]
            if False in res:
                return False
        return True

    @property
    def info(self):
        return self._info

    def toLine(self, tag=True):
        s1 = "~".join([f.value for f in self.fileds.values()]) + \
               "~" + ";".join(self.info) + "\n"
        s2 = "~".join([f.value for f in self.fileds.values()])+"\n"
        return s2 if tag else s1


if __name__ == '__main__':
    s = BiBean(["1", "2", "3", "4", "5", "6", "7", "8", "9", "11"])
    print(s)
    pass
