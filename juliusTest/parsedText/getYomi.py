import re
import sys

class mec():

    def __init__(self):
        return

    def split1(self,f):
        head=[]
        tail=[]
        i=0
        re1 = '(.+)(\s+)(.+)'

        comp = re.compile(re1)
        line = f.readline()

        while line:
            match = comp.match(line)
            head[i] = match.group(1)
            tail[i] = match.group(3)
            i =+ 1
            line = f.readline()

        return head, tail

    def split2(self,tail):
        pos=[]
        yomi=[]
        re2 = '(.+),(.+),(.+),(.+),(.+),(.+),(.+)'

        comp = re.compile(re2)

        for n in range(len(tail)):
            match = comp.match(tail[n])
            pos[n] = match.group(1)
            yomi[n] = match.group(7)

        return pos, yomi

if __name__ == "__main__":

    f = open(sys.argv[0],'r')
    c = open(sys.argv[0],'w')

    m = mec()

    head, tail = m.split1(f)

    pos, yomi = m.split2(tail)

    for i in range(len(head)):
        c.write(pos)
        c.write(' ')
        c.write(head)
        c.write(' ')
        c.write(tail)

    f.close()
    c.close()
