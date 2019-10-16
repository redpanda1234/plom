__author__ = "Andrew Rechnitzer"
__copyright__ = "Copyright (C) 2019 Andrew Rechnitzer"
__credits__ = ["Andrew Rechnitzer", "Colin Macdonald"]
__license__ = "AGPLv3"

import json
import os
import random
import subprocess
import sys

from aliceBob import aliceBob

# Stuff for hashing and verifying passwords
from passlib.hash import pbkdf2_sha256
from passlib.context import CryptContext

# Fire up password stuff
mlpctx = CryptContext(schemes=["pbkdf2_sha256", "bcrypt"], deprecated="auto")

# get canned user list
ab = aliceBob()
lst = ab.getNewList()

for (n, p) in lst:
    print(n + "\t" + p)
for (n, p) in lst:
    print('  "{}": "{}",'.format(n, mlpctx.encrypt(p)))