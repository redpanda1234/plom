#!/usr/bin/env python3

__author__ = "Andrew Rechnitzer"
__copyright__ = "Copyright (C) 2018-2019 Andrew Rechnitzer"
__credits__ = ["Andrew Rechnitzer", "Colin Macdonald", "Elvis Cai"]
__license__ = "AGPLv3"

from collections import defaultdict
import glob
import json
import os
import re
import shutil
import subprocess
import sys

# this allows us to import from ../resources
sys.path.append("..")
from resources.testspecification import TestSpecification
from resources.tpv_utils import parseTPV, isValidTPV, hasCurrentAPI, getCode, getPosition


def decodeQRs():
    """Go into pageimage directory
    Look at all the png files
    If their QRcodes have not been successfully decoded previously
    then decode them using another script.
    The results are stored in blah.png.qr files.
    Commands piped through gnu-parallel.
    """
    os.chdir("./pageImages/")
    fh = open("commandlist.txt", "w")
    for fname in glob.glob("*.png"):
        # If the .qr file does not exist, or if it has length 0
        # then run extract/orient script on that png.
        if (not os.path.exists(fname + ".qr")) or os.path.getsize(fname + ".qr") == 0:
            fh.write("python3 ../extractQR.py {}\n".format(fname))
    fh.close()
    # run those commands through gnu-parallel then delete.
    os.system("parallel --bar < commandlist.txt")
    os.unlink("commandlist.txt")
    os.chdir("../")


def readExamsProduced():
    """Read the exams that were produced during build"""
    global examsProduced
    with open("../resources/examsProduced.json") as data_file:
        examsProduced = json.load(data_file)


def readExamsScanned():
    """Read the list of test/page/versions that have been scanned"""
    global examsScanned
    if os.path.exists("../resources/examsScanned.json"):
        with open("../resources/examsScanned.json") as data_file:
            examsScanned = json.load(data_file)


def writeExamsScanned():
    """Update the list of test/page/versions that have been scanned"""
    es = open("../resources/examsScanned.json", "w")
    es.write(json.dumps(examsScanned, indent=2, sort_keys=True))
    es.close()


def reOrientPage(fname, qrs):
    """Re-orient this page if needed or fail

    TODO: would two be good enough?  Just one?
    """
    # fake a default_dict
    g = lambda x: getPosition(qrs.get(x)) if qrs.get(x, None) else -1
    if g('NE') == 1 and g('SW') == 3 and g('SE') == 4:
        pass
    elif g('NW') == 2 and g('SW') == 3 and g('SE') == 4:
        pass
    elif g('NE') == 3 and g('NW') == 4 and (g('SW') == 1 or g('SE') == 2):
        print(" .  {}: reorienting: 180 degree rotation".format(fname))
        subprocess.run(["mogrify", "-quiet", "-rotate", "180", fname],
                    stderr=subprocess.STDOUT, shell=False, check=True)
    else:
        return False
    return True


def checkQRsValid():
    """Check that the QRcodes in each pageimage are valid.

    When each png is scanned a png.qr is produced.  Load the dict of
    QR codes from that file and do some sanity checks.

    Rotate any images that we can.

    TODO: maybe we should split this function up a bit!
    """
    # go into page image directory and look at each .qr file.
    os.chdir("pageImages/")
    for fname in glob.glob("*.qr"):
        with open(fname, "r") as qrfile:
            content = qrfile.read()
        qrs = eval(content)  # unpickle

        problemFlag = False
        warnFlag = False


        # Flag papers that have too many QR codes in some corner
        # TODO: untested?
        if any(len(x) > 1 for x in qrs.values()):
            msg = "Too many QR codes in {} corner".format(d)
            problemFlag = True

        # Unpack the lists of QRs, building a new dict with only the
        # the corners with exactly one QR code.
        tmp = {}
        for (d, qr) in qrs.items():
            if len(qr) == 1:
                tmp[d] = qr[0]
        qrs = tmp
        del tmp

        if len(qrs) == 0:
            msg = "No QR codes were decoded."
            problemFlag = True

        if not problemFlag:
            for tpvc in qrs.values():
                if not isValidTPV(tpvc):
                    msg = "TPV '{}' is not a valid format".format(tpvc)
                    problemFlag = True
                elif not hasCurrentAPI(tpvc):
                    msg = "TPV '{}' does not match API.  Legacy issue?".format(tpvc)
                    problemFlag = True
                elif str(getCode(tpvc)) != str(spec.MagicCode):
                    msg = "Magic code '{0}' did not match spec '{1}'.  " \
                          "Did you scan the wrong test?".format(getCode(tpvc), spec.MagicCode)
                    problemFlag = True

        # Make sure all (t,p,v) on this page are the same
        if not problemFlag:
            tgvs = []
            for tpvc in qrs.values():
                tn, pn, vn, cn, o = parseTPV(tpvc)
                tgvs.append((tn, pn, vn))

            if not len(set(tgvs)) == 1:
                # Decoder either gives the correct code or no code at all
                # Perhaps if you see this, its a folded page
                msg = "Multiple different QR codes! (rare in theory)"
                problemFlag = True

        if not problemFlag:
            orientationKnown = reOrientPage(fname[:-3], qrs)
            # TODO: future improvement: could keep going, its possible
            # we can go on to find the (t,p,v) in many cases.
            if not orientationKnown:
                msg = 'Orientation not known'
                problemFlag = True

        # Decide in which cases we can be confident we know this papers (t,p,v)
        if not problemFlag:
            if len(tgvs) == 1:
                msg = "Only one of three QR codes decoded."
                # TODO: in principle could proceed, albeit dangerously
                warnFlag = True
                riskiness = 10
                tgv = tgvs[0]
            elif len(tgvs) == 2:
                msg = "Only two of three QR codes decoded."
                warnFlag = True
                riskiness = 1
                tgv = tgvs[0]
            elif len(tgvs) == 3:
                # full consensus
                tgv = tgvs[0]
            else:  #len > 3, shouldn't be possible now
                msg = "Too many QR codes on the page!"
                problemFlag = True

        if not problemFlag:
            # we have a valid TGVC and the code matches.
            if warnFlag:
                print("[W] {0} {1}".format(fname, msg))
                print("   (high occurences of these warnings may mean printer/scanner problems)")
            # store the tpv in examsScannedNow
            examsScannedNow[tn][pn] = (vn, fname[:-3])
            # later we check that list against those produced during build

        # TODO:
        #if orientationKnown is False:
        #    # set this after recording the tpv
        #    problemFlag = True
        #    msg = 'Orientation not known'

        if problemFlag:
            # Difficulty scanning this pageimage so move it
            # to problemimages
            print("[E] {0} {1}".format(fname, msg))
            print("    Flagging for manual inspection.")
            # move blah.png.qr
            shutil.move(fname, "problemImages")
            # move blah.png
            shutil.move(fname[:-3], "problemImages")

    os.chdir("../")


def validateQRsAgainstProduction():
    """After pageimages have been decoded we need to check the
    results against the TPVs that constructed during build.
    A simple check of test-name was done already, but now
    the test-page-version triples are checked.
    """
    # go into page images directory
    os.chdir("./pageImages")
    # for each test-number that was scanned on this run of this script
    # check that the tpv matches the one recorded during build.
    for t in examsScannedNow.keys():
        # create string of t for json matching.
        ts = str(t)
        # for each page of that test-number
        for p in examsScannedNow[t].keys():
            # again create string of p for json matching.
            ps = str(p)
            # the version of that test/page
            v = examsScannedNow[t][p][0]
            # the corresponding page image file name
            fn = examsScannedNow[t][p][1]
            # if the tpv's match then all good.
            if examsProduced[ts][ps] == v:
                # print success and thats all.
                print(
                    "Valid scan of t{:s} p{:s} v{:d} from file {:s}".format(
                        ts, ps, v, fn
                    )
                )
            else:
                # print mismatch warning and move file to problem-images
                print(">> Mismatch between exam scanned and exam produced")
                print(
                    ">> Produced t{:s} p{:s} v{:d}".format(
                        ts, ps, examsProduced[ts][ps]
                    )
                )
                print(
                    ">> Scanned t{:s} p{:s} v{:d} from file {:s}".format(ts, ps, v, fn)
                )
                print(">> Moving problem files to problemImages")
                # move the blah.png and blah.png.qr
                # this means that they won't be added to the
                # list of correctly scanned page images
                shutil.move(fn, "problemImages")
                shutil.move(fn + ".qr", "problemImages")
                # Remove page from the exams-scanned-now list.
                examsScannedNow[ts].pop(ps)
    os.chdir("../")


def addCurrentScansToExamsScanned():
    os.chdir("./pageImages")
    # For each test we have just scanned
    for t in examsScannedNow.keys():
        ts = str(t)  # for json keys
        # if it is not in the previous scan batch
        # create an entry for it.
        if ts not in examsScanned:
            examsScanned[ts] = {}
        # For each page in this test
        for p in examsScannedNow[t].keys():
            ps = str(p)  # for json keys
            # grab the version and filename
            v = examsScannedNow[t][p][0]
            fn = examsScannedNow[t][p][1]
            # If we have seen this test/page before then
            # we will overwrite the old one but issue a warning
            if ps in examsScanned[ts]:
                # Eventually we should output this sort of thing to
                # a log file in case of user-errors.
                print(
                    ">> Have already scanned t{:s}p{:s}v{:d} in file {:s}".format(
                        ts, ps, v, fn
                    )
                )
                print(">> Will overwrite with new version")
                examsScanned[ts][ps] = examsScannedNow[t][p]
            else:
                # This is a new test/page so add it to the scan-list
                examsScanned[ts][ps] = examsScannedNow[t][p]
                # copy the file into place
                # eventually we should move it instead of copying it.
                # save on disc space?
                shutil.copy(
                    fn,
                    "../decodedPages/page_{}/version_{}/t{}p{}v{}.png".format(
                        str(p).zfill(2),
                        str(v),
                        str(t).zfill(4),
                        str(p).zfill(2),
                        str(v),
                    ),
                )
            # move the filename into alreadyProcessed
            shutil.move(fn, "alreadyProcessed")
            shutil.move(fn + ".qr", "alreadyProcessed")
    os.chdir("../")


if __name__ == '__main__':
    examsProduced = {}
    examsScanned = defaultdict(dict)
    examsScannedNow = defaultdict(dict)
    spec = TestSpecification()
    spec.readSpec()
    readExamsProduced()
    readExamsScanned()
    decodeQRs()
    checkQRsValid()
    validateQRsAgainstProduction()
    addCurrentScansToExamsScanned()
    writeExamsScanned()
