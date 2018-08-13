import os,json,csv
from testspecification import TestSpecification
from collections import defaultdict
import sys
import sqlite3

sys.path.append("../imageServer")

markdb = sqlite3.connect('file:../resources/test_marks.db?mode=ro', uri=True)
curMark = markdb.cursor()

iddb = sqlite3.connect('file:../resources/identity.db?mode=ro', uri=True)
curID = iddb.cursor()

groupImagesMarked=defaultdict(lambda: defaultdict(list))
examsIDed = {}

def checkMarked(n):
    global groupImagesMarked
    for row in curMark.execute("SELECT * FROM groupimage WHERE number='{}'".format(n)):
        if row[7] != 'Marked':
            print("Not yet marked {}".format(row[3]))
            return False
        else:
            groupImagesMarked[n][row[4]] = [row[5], row[10]]
    return True

def checkIDed(n):
    global examsIDed
    for row in curID.execute("SELECT * FROM idimage WHERE number = '{}'".format(n)):
        if row[3] != 'Identified':
            print("Not yet id'd {}".row[1])
            return False
        else:
            examsIDed[n] = [row[6], row[7]] #store SID and SName
    return True


def readExamsGrouped():
    global examsGrouped
    if(os.path.exists("../resources/examsGrouped.json")):
        with open('../resources/examsGrouped.json') as data_file:
            examsGrouped = json.load(data_file)

def checkExam(n):
    print("##################\nExam {}".format(n))
    if(checkMarked(n) and checkIDed(n) ):
        print("\tComplete - build front page and reassemble.")
        return(True)
    else:
        return(False)

def writeExamsCompleted():
    fh = open("../resources/examsCompleted.json",'w')
    fh.write( json.dumps(examsCompleted, indent=2, sort_keys=True))
    fh.close()

def writeMarkCSV():
    head = ['StudentID','StudentName','TestNumber']
    for pg in range(1,spec.getNumberOfGroups()+1):
        head.append('PageGroup{} Mark'.format(pg))
    head.append('Total')
    for pg in range(1,spec.getNumberOfGroups()+1):
        head.append('PageGroup{} Version'.format(pg))

    with open("testMarks.csv", 'w') as csvfile:
        testWriter = csv.DictWriter(csvfile, fieldnames=head, delimiter='\t', quotechar="\"", quoting=csv.QUOTE_NONNUMERIC)
        testWriter.writeheader()
        for n in sorted(examsCompleted.keys()):
            if(examsCompleted[n]==False):
                continue
            ns = str(n)
            row=dict()
            row['StudentID'] = examsIDed[ns][0]
            row['StudentName'] = examsIDed[ns][1]
            row['TestNumber'] = n
            tot = 0
            for pg in range(1,spec.getNumberOfGroups()+1):
                tot += groupImagesMarked[ns][pg][1]
                row['PageGroup{} Mark'.format(pg)] = groupImagesMarked[ns][pg][1]
                row['PageGroup{} Version'.format(pg)] = groupImagesMarked[ns][pg][0]
            row['Total']=tot
            testWriter.writerow(row)

spec = TestSpecification()
spec.readSpec()

readExamsGrouped()

examsCompleted={}
for n in sorted(examsGrouped.keys()):
    examsCompleted[int(n)]=checkExam(n)

writeExamsCompleted()
writeMarkCSV()

markdb.close()
iddb.close()
