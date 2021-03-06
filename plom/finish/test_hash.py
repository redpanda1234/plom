# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2019 Colin B. Macdonald
# Copyright (C) 2020 Dryden Wiebe

from .utils import my_hash


def test_hash():
    assert my_hash("12345678", salt="salt") == "351525727036"
    assert my_hash("12345678", salt="salty") == "782385405730"
    assert my_hash("12345679", salt="salt") == "909470548567"


def test_hash_error():
    error = None
    try:
        my_hash("123456789", salt=None)
        error = False
    except ValueError:
        error = True
    assert error == True
