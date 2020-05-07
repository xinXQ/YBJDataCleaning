# _*_ coding=utf-8 _*_
import time

from preExecuteForCitys.beans.BiBean import BiBean, BiBeanFieldsLenErr
from preExecuteForCitys.beans.CbBean import CbBean, CbBeanFieldsLenErr
from preExecuteForCitys.utils.filesutils import classifyFiles

if __name__ == '__main__':
    pt = "E:/pyworkspaces/YBJ/preExecuteForCitys/testData"
    jcs = classifyFiles(pt, lambda x: x.__contains__("cbxx"))
    count = 0
    for f in jcs:
        fr = open(f, 'r', encoding='utf-8')
        for line in fr:
            count += 1
            fs = line.strip().split("~")
            try:
                bb = CbBean(fs)
            except CbBeanFieldsLenErr as e:
                print(line)
                continue
            stat = bb.check()
            if not stat:
                print("=====", "; ".join(bb.info))
            if count % 10000 == 0:
                print(count)
    print(count)
