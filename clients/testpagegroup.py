class TestPageGroup:
    def __init__(self, tgv, fname):
        #tgv = t0000p00v0
        #... = 0123456789
        self.prefix = tgv
        self.test = tgv[1:5]
        self.group = tgv[6:8]
        self.version = tgv[9]
        self.status = "untouched"
        self.mark = "-1"
        self.originalFile = fname
        self.annotatedFile = ""

    def printMe(self):
        print( [self.prefix, self.status, self.mark, self.originalFile, self.annotatedFile])

    def setstatus(self, st):
        #tgv = t0000p00v0
        #... = 0123456789
        self.status = st

    def setAnnotatedFile(self,fname):
        self.annotatedFile=fname
        self.status="flipped"

    def setReverted(self):
        self.status="reverted"
        self.mark="-1"
        self.annotatedFile=""

    def setmark(self, mrk, afname):
        #tgv = t0000p00v0
        #... = 0123456789
        self.status = "marked"
        self.mark = mrk
        self.annotatedFile=afname