# =*= coding:utf-8 =*=
# かしら
import re
import os
import os.path
import sys
import functools
import itertools

class StringSeq :
    def __init__(self, org, seq) :
        self.org = org
        self.seq = seq

    def __repr__(self) :
        return 'StringSeq<%s>' % ', '.join(repr(c) for c in self.seq)

    def __str__(self) :
        return self.normalize()
    
    def normalize(self) :
        def dispatch(c) :
            if isinstance(c, CharNum) :
                return c.normalize()
            else :
                return c

        return ''.join(dispatch(c) for c in self.seq)

class CharNum :
    def __init__(self, num) :
        self.num = num
        self.len = 0
    
    def __repr__(self) :
        return 'CharNum<%s, %d>' % (self.num, self.len)
    
    def __str__(self) :
        return self.normalize()
    
    def normalize(self) :
        return '{0:0{1}}'.format(self.num, self.len)


# rstr が大きければ 1, lstr が大きければ -1
def comp(lstr, rstr) :
    for lv, rv in itertools.zip_longest(lstr.seq, rstr.seq) :
        if lv is None :
            return -1
        elif rv is None :
            return 1

        # print('lv.num(%s) - rv.num(%s)' % (lv, rv))

        lnum = isinstance(lv, CharNum)
        rnum = isinstance(rv, CharNum)
        if lnum and rnum :
            # print('lv.num(%s) - rv.num(%s)' % (lv.num, rv.num))
            if lv.num == rv.num :
                continue
            else :
                return lv.num - rv.num
        elif not lnum and not rnum :
            # str
            if lnum == rnum :
                continue
            else :
                return 1 if rv < lv else -1
        elif lnum and not rnum :   # 左だけ数字
            return 1    # 文字のほうが大きい
        else : # not lnum and rnum
            return -1
    
    return 0

RE_NUM = re.compile(r'(\d+|[^\d])')
def parse(s) :
    def normalize(c) :
        try :
            return CharNum(int(c))
        except :
            return c

    arr = [normalize(it.group(1)) for it in RE_NUM.finditer(s)]
    return StringSeq(s, arr)

def _readFromDirectory(dirPath) :
    join   = os.path.join
    isfile = os.path.isfile

    def filterFile(file) :
        j = join(dirPath, file)
        return isfile(j)

    fileList = os.listdir(dirPath)
    fileList = filter(filterFile, fileList)

    ret = [ parse(file) for file in fileList ]
    if len(ret) == 0 :
        raise Exception("the directory not have files...")

    return ret

def _readFromFile(filePath) :
    with open(filePath, 'r', encoding='utf-8') as h :
        ret = [ parse(line.rstrip()) for line in h ]
        if len(ret) == 0 :
            raise Exception("file is empty...")
        
        return ret

def _readFromStdin() :
    ret = [ parse(line.rstrip()) for line in sys.stdin ]
    if len(ret) == 0 :
        raise Exception("Filenames are not inputted.")
    
    return ret

def read(option) :
    filePath = option.path_or_filelist
    if filePath == '-' :
        filePath = None

    if filePath :
        if os.path.isfile(filePath) :
            # specify file.
            option.print  = True
            option.move   = False
            option.backup = False
            return _readFromFile(filePath)
        elif os.path.isdir(filePath) :
            # specify directory
            if not option.print and not option.move :
                option.move = True
            return _readFromDirectory(filePath)
    else :
        option.print  = True
        option.move   = False
        option.backup = False
        return _readFromStdin()


def fitKeta(fileList) :
    def computeMaxKeta(keta) :
        if not isinstance(keta, CharNum) :
            return -1

        myLen = len('%d' % keta.num)
        return myLen

    def applyKeta(keta, length) :
        if not isinstance(keta, CharNum) :
            return
        # print(repr(keta))
        keta.len = length

    # apply
    for ketaList in itertools.zip_longest(*[file.seq for file in fileList]) :
        maxLength = max( computeMaxKeta(keta) for keta in ketaList )
        list(map(lambda keta : applyKeta(keta, maxLength), ketaList))
     
    return fileList

def backupFiles(dirPath) :
    import shutil
    print("backup files...", file=sys.stderr)
    backupDir = os.path.join(dirPath, "_backup")
    shutil.rmtree(backupDir)
    shutil.copytree(dirPath, backupDir)

def operateFile(file, dirName, bePrint, beMove) :
    fileNameOrg    = file.org
    fileNameNormal = file.normalize()

    if bePrint :
        print("{}\t{}".format(fileNameOrg, fileNameNormal))

    if beMove :
        jOrg    = os.path.join(dirName, fileNameOrg)
        jNormal = os.path.join(dirName, fileNameNormal)
        os.rename(jOrg, jNormal)

def main2(option) :
    fileList = read(option)
    fileList = sorted(fileList, key=functools.cmp_to_key(comp))
    fitKeta(fileList)

    dirName = option.path_or_filelist or ''
    def apply(file) :
        operateFile(file, dirName, option.print, option.move)
    list(map(apply, fileList))

def getOpt() :
    import argparse

    argParser = argparse.ArgumentParser()
    argParser.add_argument("-m", "--move",   help="move files (default action if set a path in path_or_filelist)", action="store_true")
    argParser.add_argument("-p", "--print",  help="print pair of (orgFileName, normalizedName). do not move files. (default action if set a filelist in path_or_filelist)", action="store_true")
    argParser.add_argument("-b", "--backup", help="backup files. copy to '_backup' directory", action="store_true")
    argParser.add_argument("path_or_filelist", nargs='?', help="target path or file list (utf-8). if no set or set '-' then read filelist from stdin.", default=[])

    return argParser.parse_args()

def main() :
    opt = getOpt()
    # print(opt)

    main2(opt)

if __name__ == '__main__' :
    main()
