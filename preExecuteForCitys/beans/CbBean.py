# _*_ coding=utf-8 _*_

"""
参保信息Bean
ADMDVS,INSU_POOLAREA,POOLAREA,PSN_NO,CERT_TYPE,CERT_NO,NAME,PSN_CLCT_STAS,INSU_STAS,
PSN_TYPE,INSU_TYPE,BEGN_YM,EXPI_YM,EMP_NO,EMP_NAME,CIS_REA
参保地医保区划名称,参保地医保区划编码,统筹区编码,人员编号,证件类型,证件号码,姓名,个人缴费状态,参保状态,
参保身份,险种类型,缴费起始年月,缴费截止年月,单位编号,单位名称,参保状态变更原因
"""
from datetime import date

from beans.Field import Field
from check.CheckFuncs import res, pd, isIdCard
from utils.CheckByFieldName import cbRole


class CbBeanFieldsLenErr(Exception):
    pass


class CbBean:
    _fields = ["ADMDVS", "INSU_POOLAREA", "POOLAREA", "PSN_NO", "CERT_TYPE",
               "CERT_NO", "NAME", "PSN_CLCT_STAS", "INSU_STAS", "PSN_TYPE",
               "INSU_TYPE", "BEGN_YM", "EXPI_YM", "EMP_NO", "EMP_NAME", "CIS_REA"]

    # 将字段封装到Field对象里面
    def __init__(self, fields):
        if len(fields) != len(self._fields):
            raise CbBeanFieldsLenErr("参保信息数据字段异常")
        self._info = []
        self.fileds = {self._fields[x]: Field(self._fields[x], fields[x]) for x in range(len(self._fields))}

    def __str__(self):
        return "\n".join([str(f) for f in self.fileds])

    __repr__ = __str__

    # 将每个field根据规范进行检查
    def checkAllFields(self):
        for k, v in self.fileds.items():
            res = [r(v) for r in cbRole[k]]
            if False in res:
                return False
        return True

    # 终止参保条件下，缴费状态必须为暂停缴费或终止缴费。
    def checkPcsWhenIsEquF(self):
        ins = self.fileds["INSU_STAS"]
        pcs = self.fileds["PSN_CLCT_STAS"]
        assert isinstance(ins, Field)
        assert isinstance(pcs, Field)
        return pcs.value == "2" or pcs.value == "3" if ins.value == "4" else True

    """
    # 参保地行政区划编码与参保地行政区划名称必须匹配。
    # 统筹区编码与参保地行政区划编码需对应匹配。
    参保地行政区划名称和区划匹配是字典里面一一对应的，
    统筹区是包括参保地行政区划,就比如参保地是庐阳区,统筹区可以是庐阳区或者合肥市或者安徽省
    """

    def checkAreaMatching(self):
        adm = self.fileds["ADMDVS"]
        ip = self.fileds["INSU_POOLAREA"]
        pa = self.fileds["POOLAREA"]
        assert isinstance(adm, Field)
        assert isinstance(ip, Field)
        assert isinstance(pa, Field)
        poa = pd.parseData["POOLAREA"]
        flag = True if ip.value in poa and poa[ip.value] == adm.value else False
        if ip.value != pa.value and ip.value in res and pa.value != res[ip.value]:
            flag = False
        return flag

    """
    退休职工 11,在职职工 10: 城镇职工基本医疗保险 11,生育保险 31 (不能参加"其他险种")
    # 灵活就业人员(其他身份) 99: 城镇职工基本医疗保险,生育险
    其他人员 99: 其他险种
    离休 12: 不限,包括生育险
    居民 21: 城乡居民基本医疗保险 21
    """

    def checkItPtMatching(self):
        it = self.fileds["INSU_TYPE"]
        pt = self.fileds["PSN_TYPE"]
        assert isinstance(it, Field)
        assert isinstance(pt, Field)
        itt = it.value
        switch = {
            "10": itt == "11" or itt == "31",
            "11": itt == "11" or itt == "31",
            "12": True,
            "21": itt == "21",
            "99": itt == "99",
        }
        if pt.value not in switch:
            return False
        return switch[pt.value]

    """
    正常参保,正常缴费,参保身份时10,11,12, 截至时间必须为空
    参保身份是21 或者 参保状态是4 或者 缴费状态是2 截至时间必须不为空, 并且截至时间必须大于等于开始时间 
    """
    def checkYm(self):
        ins = self.fileds["INSU_STAS"]
        pcs = self.fileds["PSN_CLCT_STAS"]
        by = self.fileds["BEGN_YM"]
        ey = self.fileds["EXPI_YM"]
        pt = self.fileds["PSN_TYPE"]
        assert isinstance(ins, Field)
        assert isinstance(pcs, Field)
        assert isinstance(by, Field)
        assert isinstance(ey, Field)
        assert isinstance(pt, Field)
        if ins.value == "1" and pcs.value == "1" and (pt.value == "11" or pt.value == "10" or pt.value == "12"):
            return ey.value is None or "" == ey.value
        if pt.value == "21" or ins.value == "4" or pcs.value == "2":
            try:
                byd = date(int(by.value[:4]), int(by.value[4:6]), 1)
                eyd = date(int(ey.value[:4]), int(ey.value[4:6]), 1)
                return byd <= eyd
            except Exception as e:
                return False
        return True

    # 基础信息表的内部关联检查 !!
    def idCardCheck(self):
        ct = self.fileds["CERT_TYPE"]
        cn = self.fileds["CERT_NO"]
        assert isinstance(ct, Field)
        assert isinstance(cn, Field)
        # 1,当证件类型为居民身份证（户口簿）时，证件号码必须为18位,并且必须符合身份证校验规则，包括性别、出生日期和校验位。
        # 2,当证件号码为合法身份证时，证件类型必须为居民身份证（户口簿）。
        a = isIdCard(cn)
        return (a and "01" == ct.value) or (not a and "01" != ct.value)

    # 获取这个bean的最终结果
    def check(self):
        allFieldsStat = self.checkAllFields()
        pcsWhenIsEquFStat = self.checkPcsWhenIsEquF()
        if not pcsWhenIsEquFStat:
            self._info.append("终止参保条件下,缴费状态必须为暂停缴费或终止缴费")
        areaMatchingStat = self.checkAreaMatching()
        if not areaMatchingStat:
            self._info.append("参保地行政区划编码,行政区划名称,统筹区编码必须匹配")
        itPtMatchingStat = self.checkItPtMatching()
        if not itPtMatchingStat:
            self._info.append("参保身份和参保类型必须匹配")
        idCardStat = self.idCardCheck()
        if not idCardStat:
            self._info.append("证件类型和证件号码必须匹配")
        ymStat = self.checkYm()
        if not ymStat:
            self._info.append("开始时间和截至时间不符合逻辑")
        self._info.extend([f.info for f in self.fileds.values()])
        self._info = [x for x in self._info if x != ""]
        return allFieldsStat and pcsWhenIsEquFStat and areaMatchingStat \
               and itPtMatchingStat and ymStat and idCardStat

    @property
    def info(self):
        return self._info

    def toLine(self, tag=True):
        s1 = "~".join([f.value for f in self.fileds.values()]) + \
             "~" + ";".join(self.info) + "\n"
        s2 = "~".join([f.value for f in self.fileds.values()]) + "\n"
        return s2 if tag else s1


if __name__ == '__main__':
    cb = CbBean(["1", "2", "3", "4", "5", "6", "7", "8", "9", "11", "12", "13", "14", "15", "16", "17"])
    print(cb)
