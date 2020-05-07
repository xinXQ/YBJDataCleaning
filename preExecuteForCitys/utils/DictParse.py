# _*_ coding=utf-8 _*_

"""
将字典文件变成字典
单例模式
"""
import os


class DictParse:
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            orgi = super(DictParse, cls)
            cls._instance = orgi.__new__(cls)
        return cls._instance

    def __init__(self):
        self.p = os.path.dirname(__file__)

        def initSingleData(path, index=0):
            fileHandle = open(path, 'r', encoding='utf-8')
            dataset = set()
            for line in fileHandle.readlines():
                dataset.add(line.strip().split("\t")[index])
            return dataset

        def initMultiData(path):
            fileHandle = open(path, 'r', encoding='utf-8')
            regionDict = {}
            for line in fileHandle.readlines():
                line = line.strip()
                ss = line.split("\t")[-2:]
                regionDict[ss[0]] = ss[1]
            return regionDict

        self.regionDict = {}
        self.parseData = {
            "NATY": initSingleData(self.p + "/../dictfiles/ethnic_type.tsv"),
            "GEND": initSingleData(self.p + "/../dictfiles/gender_type.tsv"),
            "CERT_TYPE": initSingleData(self.p + "/../dictfiles/id_type.tsv"),
            "INSU_TYPE": initSingleData(self.p + "/../dictfiles/insurance_type.tsv"),
            "PSN_TYPE": initSingleData(self.p + "/../dictfiles/insured_id_type.tsv"),
            "INSU_STAS": initSingleData(self.p + "/../dictfiles/insured_status_type.tsv"),
            "SURV_STAS": initSingleData(self.p + "/../dictfiles/live_status_type.tsv"),
            "PSN_CLCT_STAS": initSingleData(self.p + "/../dictfiles/payment_status.tsv"),
            "NAT_REGN_CODE": initSingleData(self.p + "/../dictfiles/nation_type.tsv"),
            "CIS_REA": initSingleData(self.p + "/../dictfiles/change_reason.tsv"),
            "NAT_REGN_NAME": initSingleData(self.p + "/../dictfiles/nation_type.tsv", 1),
            "POOLAREA": initMultiData(self.p + "/../dictfiles/region.tsv"),
            "INSU_POOLAREA": initMultiData(self.p + "/../dictfiles/region.tsv"),
            "ADMDVS": set(initMultiData(self.p + "/../dictfiles/region.tsv").values())
        }

    def areaMatching(self):
        pa = {x: v for x, v in self.parseData['POOLAREA'].items() if x.startswith("34")}
        res = {}
        for k, v in pa.items():
            if k.endswith("00"):
                pk = None
            else:
                pk = k[:4] + '00'
            res[k] = pk
        return res


if __name__ == '__main__':
    # b = DictParse()
    a = DictParse()
    # print(id(a.regionDict), id(b.regionDict))
    # print(a.parseData)
    a.t()
