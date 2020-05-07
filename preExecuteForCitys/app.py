import os
import sys, getopt

from preExecuteForCitys.beans.BiBean import BiBean, BiBeanFieldsLenErr
from preExecuteForCitys.beans.CbBean import CbBean
from preExecuteForCitys.utils.filesutils import classifyFiles, FileUtil


def parsePara(argv):
    inputfile = ''
    outputfile = ''
    try:
        opts, args = getopt.getopt(argv, "hi:o:", ["ifile=", "ofile="])
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
    return inputfile, outputfile


def executeJc(inputFile, outputFile):
    files = classifyFiles(inputFile, lambda x: x.__contains__("jcxx"))
    fu = FileUtil(outputFile)
    for file in files:
        fus = fu.getWriteFilePath(file, "out", "err-{}".format(os.path.basename(file)))
        fr = open(file, 'r', encoding='utf-8', errors='ignore')
        print(fus.errPath, fus.filePath)
        fw = open(fus.filePath, 'a', encoding='utf-8')
        fe = open(fus.errPath, 'a', encoding='utf-8')
        for line in fr:
            fields = line.strip().split("~")
            try:
                bb = BiBean(fields)
                stat = bb.check()
                if stat:
                    fw.write(bb.toLine())
                else:
                    fe.write(bb.toLine(False))
            except BiBeanFieldsLenErr as e:
                fe.write(line.strip()+"~字段数量不对\n")
                continue


def executeCb(inputFile, outputFile):
    files = classifyFiles(inputFile, lambda x: x.__contains__("cbxx"))
    fu = FileUtil(outputFile)
    for file in files:
        fus = fu.getWriteFilePath(file, "out", "err-{}".format(os.path.basename(file)))
        fr = open(file, 'r', encoding='utf-8', errors='ignore')
        print(fus.errPath, fus.filePath)
        fw = open(fus.filePath, 'a', encoding='utf-8')
        fe = open(fus.errPath, 'a', encoding='utf-8')
        for line in fr:
            fields = line.strip().split("~")
            try:
                bb = CbBean(fields)
                stat = bb.check()
                if stat:
                    fw.write(bb.toLine())
                else:
                    fe.write(bb.toLine(False))
            except BiBeanFieldsLenErr as e:
                fe.write(line.strip() + "~字段数量不对\n")
                continue


if __name__ == "__main__":
    # inputFile, outputFile = parsePara(sys.argv[1:])
    executeJc("E:/pyworkspaces/YBJ/preExecuteForCitys/testData/",
              "E:/pyworkspaces/YBJ/preExecuteForCitys/out/")
    executeCb("E:/pyworkspaces/YBJ/preExecuteForCitys/testData/",
              "E:/pyworkspaces/YBJ/preExecuteForCitys/out/")
