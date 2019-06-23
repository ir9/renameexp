# =*= coding:utf-8 =*=
# かしら
import re
import sys
import functools
import itertools

class StringSeq :
    def __init__(self, seq) :
        self.seq = seq

    def __repr__(self) :
        return 'StringSeq<%s>' % ', '.join(repr(c) for c in self.seq)

    def __str__(self) :
        return ''.join(str(c) for c in self.seq)

class CharNum :
    def __init__(self, num) :
        self.num = num
        self.len = 0
    
    def __repr__(self) :
        return 'CharNum<%s, %d>' % (self.num, self.len)
    
    def __str__(self) :
        return '{0:0{1}}'.format(self.num, self.len)


def comp(lstr, rstr) :
    for lv, rv in itertools.zip_longest(lstr.seq, rstr.seq) :
        if lv is None :
            return -1
        elif rv is None :
            return 1

        lnum = isinstance(lv, CharNum)
        rnum = isinstance(rv, CharNum)
        # print('lv.num(%s) - rv.num(%s)' % (lv, rv))
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
                return rv < lv
        elif lnum and not rnum :   # 左だけ数字
            return 1
        else : # not lnum and rnum
            return -1

RE_NUM = re.compile(r'(\d+|[^\d])')
def parse(s) :
    def normalize(c) :
        try :
            return CharNum(int(c))
        except :
            return c

    arr = [normalize(it.group(1)) for it in RE_NUM.finditer(s)]
    return StringSeq(arr)

def read() :
    return [ parse(line.rstrip()) for line in sys.stdin ]


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


def main() :
    fileList = read()
    fileList = sorted(fileList, key=functools.cmp_to_key(comp))
    fitKeta(fileList)

    for file in fileList :
        print(str(file))

if __name__ == '__main__' :
    main()
