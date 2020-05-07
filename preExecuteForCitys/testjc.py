# _*_ coding=utf-8 _*_
import time

from preExecuteForCitys.beans.BiBean import BiBean, BiBeanFieldsLenErr
from preExecuteForCitys.utils.filesutils import classifyFiles

if __name__ == '__main__':
    pt = "E:/pyworkspaces/YBJ/preExecuteForCitys/testData"
    jcs = classifyFiles(pt, lambda x: x.__contains__("jcxx"))
    count = 0
    for f in jcs:
        fr = open(f, 'r', encoding='utf-8')
        for line in fr:
            count += 1
            fs = line.strip().split("~")
            try:
                bb = BiBean(fs)
            except BiBeanFieldsLenErr as e:
                print(line)
                continue
            stat = bb.check()
            if not stat:
                print(f)
                print("; ".join(bb.info))
            if count % 10000 == 0:
                print(count)
    print(count)
