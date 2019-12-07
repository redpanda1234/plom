#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "Andrew Rechnitzer"
__copyright__ = "Copyright (C) 2019 Andrew Rechnitzer and Colin Macdonald"
__credits__ = ["Andrew Rechnitzer", "Colin Macdonald"]
__license__ = "AGPL-3.0-or-later"
# SPDX-License-Identifier: AGPL-3.0-or-later

print("To start the scan process")
print("0. Copy your PDF scans of the tests into the directory scannedExams")
print("1. Copy verifiedSpec.toml from the build directory to here.")
print(
    '2. Run the "012_scansToImages.py" script - this processes your PDFs into individual pages'
)
print(
    '3. Run the "013_readQRCodes.py" script - this reads barcodes from the pages and files them away accordingly'
)
print("4. Profit")
