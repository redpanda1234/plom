#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "Andrew Rechnitzer"
__copyright__ = "Copyright (C) 2020 Andrew Rechnitzer"
__credits__ = ["Andrew Rechnitzer", "Colin Macdonald"]
__license__ = "AGPL-3.0-or-later"
# SPDX-License-Identifier: AGPL-3.0-or-later

import argparse
import getpass
import json
import os
import random
import sys
import tempfile
import toml

from PyQt5.QtCore import Qt, QPointF, QRectF
from PyQt5.QtGui import QPainterPath, QPen
from PyQt5.QtWidgets import QApplication, QWidget

from plom.plom_exceptions import *
from plom.client.pageview import PageView
from plom.client.pagescene import PageScene
from plom import AnnFontSizePts

from plom.client.tools import (
    DeltaItem,
    GroupDTItem,
)
from plom.client.tools.delete import CommandDelete
from plom.client.tools import *

from plom import __version__, Plom_API_Version
from plom.messenger import Messenger


# -------------------------------------------
# This is a very very cut-down version of annotator
# So we can automate some random marking of papers


class SceneParent(QWidget):
    def __init__(self):
        super(SceneParent, self).__init__()
        self.view = PageView(self)
        self.negComments = ["Careful", "Algebra", "Arithmetic", "Sign error", "Huh?"]
        self.posComments = ["Nice", "Well done", "Good", "Clever approach"]
        self.ink = QPen(Qt.red, 2)

    def doStuff(self, imageNames, saveName, maxMark, markStyle):
        self.saveName = saveName
        self.imageFiles = imageNames
        self.markStyle = markStyle
        self.maxMark = maxMark
        if markStyle == 2:
            self.score = 0
        else:
            self.score = maxMark

        self.scene = PageScene(
            self, imageNames, saveName, maxMark, self.score, markStyle
        )
        self.view.connectScene(self.scene)

    def getComments(self):
        return self.scene.getComments()

    def saveMarkerComments(self):
        commentList = self.getComments()
        # savefile is <blah>.png, save comments as <blah>.json
        with open(self.saveName[:-3] + "json", "w") as commentFile:
            json.dump(commentList, commentFile)

    def pickleIt(self):
        lst = self.scene.pickleSceneItems()  # newest items first
        lst.reverse()  # so newest items last
        plomDict = {
            "fileNames": [os.path.basename(fn) for fn in self.imageFiles],
            "saveName": os.path.basename(self.saveName),
            "markStyle": self.markStyle,
            "maxMark": self.maxMark,
            "currentMark": self.score,
            "sceneItems": lst,
        }
        # save pickled file as <blah>.plom
        plomFile = self.saveName[:-3] + "plom"
        with open(plomFile, "w") as fh:
            json.dump(plomDict, fh)

    def rpt(self):
        return QPointF(
            random.randint(100, 800) / 1000 * self.X,
            random.randint(100, 800) / 1000 * self.Y,
        )

    def TQX(self):
        c = random.choice([CommandTick, CommandCross, CommandQMark])
        self.scene.undoStack.push(c(self.scene, self.rpt()))

    def BE(self):
        c = random.choice([CommandBox, CommandEllipse])
        self.scene.undoStack.push(c(self.scene, QRectF(self.rpt(), self.rpt())))

    def LA(self):
        c = random.choice([CommandArrow, CommandLine, CommandArrowDouble])
        self.scene.undoStack.push(c(self.scene, self.rpt(), self.rpt()))

    def PTH(self):
        pth = QPainterPath()
        pth.moveTo(self.rpt())
        for k in range(random.randint(1, 4)):
            pth.lineTo(self.rpt())
        c = random.choice([CommandPen, CommandHighlight, CommandPenArrow])
        self.scene.undoStack.push(c(self.scene, pth))

    def GDT(self):
        blurb = TextItem(self, AnnFontSizePts)
        dlt = random.choice([1, -1])
        if self.markStyle == 2:  # mark up
            dlt *= random.randint(0, self.maxMark - self.scene.score) // 2
            if dlt <= 0:  # just text
                blurb.setPlainText(random.choice(self.negComments))
                blurb.setPos(self.rpt())
                self.scene.undoStack.push(CommandText(self.scene, blurb, self.ink))
            else:
                blurb.setPlainText(random.choice(self.posComments))
                self.scene.undoStack.push(
                    CommandGDT(self.scene, self.rpt(), dlt, blurb, AnnFontSizePts)
                )
        else:  # mark up
            dlt *= random.randint(0, self.scene.score) // 2
            if dlt >= 0:  # just text
                blurb.setPlainText(random.choice(self.posComments))
                blurb.setPos(self.rpt())
                self.scene.undoStack.push(CommandText(self.scene, blurb, self.ink))
            else:
                blurb.setPlainText(random.choice(self.negComments))
                self.scene.undoStack.push(
                    CommandGDT(self.scene, self.rpt(), dlt, blurb, AnnFontSizePts)
                )

    def doRandomAnnotations(self):
        br = self.scene.underImage.boundingRect()
        self.X = br.width()
        self.Y = br.height()

        for k in range(8):
            random.choice([self.TQX, self.BE, self.LA, self.PTH])()
        for k in range(5):
            self.GDT()
        # add comment about radom annotations
        blurb = TextItem(self, AnnFontSizePts)
        blurb.setPlainText("Random annotations for testing only.")
        blurb.setPos(QPointF(200, 100))
        self.scene.undoStack.push(CommandText(self.scene, blurb, self.ink))

    def doneAnnotating(self):
        plomFile = self.saveName[:-3] + "plom"
        commentFile = self.saveName[:-3] + "json"
        self.scene.save()
        # Save the marker's comments
        self.saveMarkerComments()
        # Pickle the scene as a plom-file
        self.pickleIt()
        return self.scene.score

    def changeMark(self, delta):
        self.score += delta


def annotatePaper(maxMark, task, imageList, aname, tags):
    print("Do stuff to task ", task)
    print("Tags are ", tags)
    # Image names = "<task>.<imagenumber>.<ext>"
    try:
        with tempfile.TemporaryDirectory() as td:
            inames = []
            for i in range(len(imageList)):
                tmp = os.path.join(td, "{}.{}.image".format(task, i))
                inames.append(tmp)
                with open(tmp, "wb+") as fh:
                    fh.write(imageList[i])
            annot = SceneParent()
            annot.doStuff(inames, aname, maxMark, random.choice([2, 3]))
            annot.doRandomAnnotations()
            return annot.doneAnnotating()
    except Exception as e:
        print("Error making random annotations to task {} = {}".format(task, e))
        exit(1)


def startMarking(question, version):
    print("Start work on question {} version {}".format(question, version))
    maxMark = messenger.MgetMaxMark(question, version)
    print("Maximum mark = ", maxMark)
    k = 0
    while True:
        task = messenger.MaskNextTask(question, version)
        if task is None:
            print("No more tasks.")
            break
        # print("Trying to claim next ask = ", task)
        try:
            print("Marking task ", task)
            imageList, image_ids, tags, integrity_check = messenger.MclaimThisTask(task)
        except PlomTakenException as e:
            print("Another user got that task. Trying again.")
            continue

        with tempfile.TemporaryDirectory() as td:
            aFile = os.path.join(td, "argh.png")
            plomFile = aFile[:-3] + "plom"
            commentFile = aFile[:-3] + "json"
            score = annotatePaper(maxMark, task, imageList, aFile, tags)
            print("Score of {} out of {}".format(score, maxMark))
            messenger.MreturnMarkedTask(
                task,
                question,
                version,
                score,
                random.randint(1, 20),
                "",
                aFile,
                plomFile,
                commentFile,
                integrity_check,
                image_ids,
            )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Perform marking tasks randomly, generally for testing."
    )

    parser.add_argument("-w", "--password", type=str)
    parser.add_argument("-u", "--user", type=str)
    parser.add_argument(
        "-s",
        "--server",
        metavar="SERVER[:PORT]",
        action="store",
        help="Which server to contact.",
    )
    global messenger
    args = parser.parse_args()
    if args.server and ":" in args.server:
        s, p = args.server.split(":")
        messenger = Messenger(s, port=p)
    else:
        messenger = Messenger(args.server)
    messenger.start()

    # If user not specified then default to scanner
    if args.user is None:
        user = "scanner"
    else:
        user = args.user

    # get the password if not specified
    if args.password is None:
        pwd = getpass.getpass("Please enter the '{}' password:".format(user))
    else:
        pwd = args.password

    # get started
    try:
        messenger.requestAndSaveToken(user, pwd)
    except PlomExistingLoginException:
        print(
            "You appear to be already logged in!\n\n"
            "  * Perhaps a previous session crashed?\n"
            "  * Do you have another scanner-script running,\n"
            "    e.g., on another computer?\n\n"
            "This script has automatically force-logout'd that user."
        )
        messenger.clearAuthorisation(user, pwd)
        exit(1)

    spec = messenger.get_spec()

    # Headless QT: https://stackoverflow.com/a/35355906
    L = sys.argv
    L.extend(["-platform", "offscreen"])
    app = QApplication(L)

    for q in range(1, spec["numberOfQuestions"] + 1):
        for v in range(1, spec["numberOfVersions"] + 1):
            print("Annotating question {} version {}".format(q, v))
            try:
                startMarking(q, v)
            except Exception as e:
                print("Error marking q.v {}.{}: {}".format(q, v, e))
                exit(1)

    messenger.closeUser()
    messenger.stop()

    exit(0)
