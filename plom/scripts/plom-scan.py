#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import os
import shutil


def clearLogin():
    print('Clear "scanner" login from server.')
    print("Not working yet.")


def scanStatus():
    print("Get scanning status report from server.")
    print("Not working yet.")


def uploadImages(unknowns=False, collisions=False):
    print("Upload images to server")
    if unknowns:
        print("Also upload unknowns")
    if collisions:
        print("Also collisions unknowns")
    print("Not working yet.")


def processScans(PDFs):
    from plom.scan import scansToImages

    # make PDF archive directory
    os.makedirs("archivedPDFs", exist_ok=True)
    # make a directory into which our (temp) PDF->PNG will go
    os.makedirs("scanPNGs", exist_ok=True)
    # finally a directory into which pageImages go
    os.makedirs("pageImages", exist_ok=True)

    # first check that we can find all the files
    for fname in PDFs:
        if not os.path.isfile(fname):
            print("Cannot find file {} - skipping".format(fname))
            continue
        print("Processing PDF {} to images".format(fname))
        scansToImages.processScans(fname)


def readImages(server, password):
    from plom.scan import readQRCodes

    # make decodedPages and unknownPages directories
    os.makedirs("decodedPages", exist_ok=True)
    os.makedirs("unknownPages", exist_ok=True)
    readQRCodes.processPNGs(server, password)


parser = argparse.ArgumentParser()
sub = parser.add_subparsers(help="sub-command help", dest="command")
#
spP = sub.add_parser("process", help="Process scanned PDFs to images.")
spR = sub.add_parser("read", help="Read QR-codes from images and collate.")
spU = sub.add_parser("upload", help="Upload page images to scanner")
spS = sub.add_parser("status", help="Get scanning status report from server")
spC = sub.add_parser("clear", help="Clear 'scanner' login.")
#
spP.add_argument("scanPDF", nargs="+", help="The PDF(s) containing scanned pages.")
spU.add_argument(
    "-u",
    "--unknowns",
    action="store_true",
    help="Upload 'unknowns'. Unknowns are pages from which the QR-codes could not be read.",
)
spU.add_argument(
    "-c",
    "--collisions",
    action="store_true",
    help="Upload 'collisions'. Collisions are pages which appear to be already on the server. You should not need this option except under exceptional circumstances.",
)
# server + password stuff
parser.add_argument(
    "-w",
    "--password",
    type=str,
    help='Password of "scanner". Not needed for "process" subcommand',
)
parser.add_argument(
    "-s",
    "--server",
    metavar="SERVER[:PORT]",
    action="store",
    help='Which server to contact. Not needed for "process" subcommand',
)
# Now parse things
args = parser.parse_args()

if args.command == "process":
    processScans(args.scanPDF)
elif args.command == "read":
    readImages(args.server, args.password)
elif args.command == "upload":
    uploadImages(args.unknowns, args.collisions)
elif args.command == "status":
    scanStatus()
elif args.command == "clear":
    clearLogin()
else:
    parser.print_help()
exit(0)
