import getopt
import os
import sys
#
# BASE_DIR = os.path.dirname(os.path.abspath(__file__))#存放c.py所在的绝对路径
# sys.path.append(BASE_DIR)
from beans.BiBean import BiBean, BiBeanFieldsLenErr
from beans.CbBean import CbBean
from utils.filesutils import classifyFiles, FileUtil

from beans.CbBean import CbBeanFieldsLenErr


def parsePara(argv):
    inputfile = ''
    outputfile = ''
    encoding = "utf-8"
    try:
        opts, args = getopt.getopt(argv, "hi:o:e:", ["ifile=", "ofile=", "encoding="])
    except getopt.GetoptError:
        print("python3", __file__, ' -i <inputfile> -o <outputfile>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('python3 {} -i <inputfile> -o <outputfile>'.format(__file__))
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputfile = arg
        elif opt in ("-o", "--ofile"):
            outputfile = arg
        elif opt in ("-e", "--encoding"):
            encoding = arg
    return inputfile, outputfile, encoding


def executeJc(inputFile, outputFile, encoding="utf-8"):
    files = classifyFiles(inputFile, lambda x: x.__contains__("jcxx"))
    fu = FileUtil(outputFile)
    count = 0
    for file in files:
        rl = []
        el = []
        fus = fu.getWriteFilePath(file, "out", "err-{}".format(os.path.basename(file)))
        fr = open(file, 'r', encoding=encoding, errors='ignore')
        print(fus.errPath, fus.filePath)
        fw = open(fus.filePath, 'a', encoding="utf-8")
        fe = open(fus.errPath, 'a', encoding="utf-8")
        for line in fr:
            count += 1
            fields = line.strip().split("~")
            try:
                bb = BiBean(fields)
                stat = bb.check()
                if stat:
                    rl.append(bb.toLine())
                else:
                    el.append(bb.toLine(False))
            except BiBeanFieldsLenErr as e:
                el.append(line.strip() + "~字段数量不对\n")
                continue
            if count % 10000 == 0:
                print(file, count)
                fw.writelines(rl)
                rl = []
                fe.writelines(el)
                el = []
        fw.writelines(rl)
        fe.writelines(el)
        fw.close()
        fe.close()


def executeCb(inputFile, outputFile, encoding="utf-8"):
    files = classifyFiles(inputFile, lambda x: x.__contains__("cbxx"))
    fu = FileUtil(outputFile)
    count = 0
    for file in files:
        rl = []
        el = []
        fus = fu.getWriteFilePath(file, "out", "err-{}".format(os.path.basename(file)))
        fr = open(file, 'r', encoding=encoding, errors='ignore')
        print(fus.errPath, fus.filePath)
        fw = open(fus.filePath, 'a', encoding='utf-8')
        fe = open(fus.errPath, 'a', encoding='utf-8')
        for line in fr:
            count += 1
            fields = line.strip().split("~")
            try:
                bb = CbBean(fields)
                stat = bb.check()
                if stat:
                    rl.append(bb.toLine())
                else:
                    el.append(bb.toLine(False))
            except CbBeanFieldsLenErr as e:
                el.append(line.strip() + "~字段数量不对\n")
                continue
            if count % 10000 == 0:
                print(file, count)
                fw.writelines(rl)
                rl = []
                fe.writelines(el)
                el = []
        fw.writelines(rl)
        fe.writelines(el)
        fw.close()
        fe.close()


if __name__ == "__main__":
    inputFile, outputFile, encoding = parsePara(sys.argv[1:])
    executeJc(inputFile, outputFile, encoding)
    executeCb(inputFile, outputFile, encoding)
