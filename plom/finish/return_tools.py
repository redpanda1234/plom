# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2018-2020 Colin B. Macdonald
# Copyright (C) 2020 Matthew Coles
# Copyright (C) 2020 Andrew Rechnitzer
# Copyright (C) 2020 Dryden Wiebe

"""Misc tools related to digital return.

Most of the Canvas-related functions are overly UBC-specific or fragile.
"""

__copyright__ = "Copyright (C) 2018-2020 Colin B. Macdonald, Matthew Coles, and others"
__license__ = "AGPL-3.0-or-later"

import os

import pandas

from plom.finish import CSVFilename
from .utils import my_hash, my_secret


def import_canvas_csv(canvas_fromfile):
    """Imports a student information from canvas.

    Args:
        canvas_fromfile (str): name of the csv file from Canvas.

    Returns:
        pandas.DataFrame : dataframe of the student information from the Canvas csv file.
    """
    df = pandas.read_csv(canvas_fromfile, dtype="object")
    print('Loading from Canvas csv file: "{0}"'.format(canvas_fromfile))

    # Note: Canvas idoicy whereby "SIS User ID" is same as "Student Number"
    cols = ["Student", "ID", "SIS User ID", "SIS Login ID", "Section", "Student Number"]
    assert all(
        [c in df.columns for c in cols]
    ), "CSV file missing columns?  We need:\n  " + str(cols)

    print(
        'Carefully filtering rows w/o "Student Number" including:\n'
        '  almost blank rows, "Points Possible" and "Test Student"s'
    )
    isbad = df.apply(
        lambda x: (
            pandas.isnull(x["SIS User ID"])
            and (
                pandas.isnull(x["Student"])
                or x["Student"].strip().lower().startswith("points possible")
                or x["Student"].strip().lower().startswith("test student")
            )
        ),
        axis=1,
    )
    df = df[isbad == False]

    return df


def find_partial_column_name(df, parthead, at_start=True):
    """Finds columns in a DataFrame that includes a specific string.

    Args:
        df (pandas.DataFrame): the dataframe that we get the column from.
        parthead (str): the first part of the column name(s) we are interested.
        at_start (bool, optional): if True we search for parthead from the begining of the column name, if False then parthead can be anywhere in the column name. Defaults to True.

    Raises:
        ValueError: If there are no possible matches (or no unique matches).

    Returns:
        pandas.DataFrame: the column(s) we are interested in.
    """
    parthead = parthead.lower()
    if at_start:
        print('Searching for column starting with "{0}":'.format(parthead))
        possible_matches = [s for s in df.columns if s.lower().startswith(parthead)]
    else:
        print('Searching for column containing "{0}":'.format(parthead))
        possible_matches = [s for s in df.columns if s.lower().find(parthead) >= 0]
    print("  We found: " + str(possible_matches))
    try:
        (col,) = possible_matches
    except ValueError as e:
        raise ValueError(
            'Column match for "{}" not found/not unique'.format(parthead)
        ) from None
    return col


def make_canvas_gradefile(canvas_fromfile, canvas_tofile, test_parthead="Test"):
    """Makes a csv file appropriate for canvas including the hashed student numbers.

    Args:
        canvas_fromfile (str): name of the csv file containing student information from canvas.
        canvas_tofile (str): name of the csv file we are writing the marks to.
        test_parthead (bool, optional): if True we search for parthead from the begining of the column name, if False then parthead can be anywhere in the column name. Defaults to True.

    Returns:
        pandas.DataFrame : the dataframe with student information (it is also written to a csv).
    """
    print("*** Generating Grade Spreadsheet ***")
    df = import_canvas_csv(canvas_fromfile)

    cols = ["Student", "ID", "SIS User ID", "SIS Login ID", "Section", "Student Number"]

    testheader = find_partial_column_name(df, test_parthead)
    cols.append(testheader)

    print("Extracting the following columns:\n  " + str(cols))
    df = df[cols]

    if not all(df[testheader].isnull()):
        print(
            '\n*** WARNING *** Target column "{0}" is not empty!\n'.format(testheader)
        )
        print(df[testheader])
        input("Press Enter to continue and overwrite...")

    print('Loading "{}" data'.format(CSVFilename))
    # TODO: should we be doing all this whereever the csv file is created?
    marks = pandas.read_csv(CSVFilename, dtype="object")

    # Make dict: this looks fragile, try merge instead...
    # marks = marks[['StudentID', 'Total']].set_index("StudentID").to_dict()
    # marks = marks['Total']
    # df['Student Number'] = df['Student Number'].map(int)
    # df[testheader] = df['Student Number'].map(marks)

    dfID = df["Student Number"].tolist()
    marksID = marks["StudentID"].tolist()
    diffList = list(set(marksID).difference(dfID))
    if diffList:
        print("")
        print("*" * 72)
        print("Warning: the following students do not appear in the Canvas sheet:")
        print(", ".join(diffList))
        print('Continuing with "Left Merge": students above may be lost in the output!')
        print("*" * 72)
        print("")
    else:
        print('All students found in Canvas. Performing "Left Merge"')

    df = pandas.merge(
        df, marks, how="left", left_on="SIS User ID", right_on="StudentID"
    )
    df[testheader] = df["Total"]
    df = df[cols]  # discard again (e.g., PG specific stuff)

    print('Writing grade data "{0}"'.format(canvas_tofile))
    # index=False: don't write integer index for each line
    df.to_csv(canvas_tofile, index=False)
    return df


def csv_add_return_codes(csvin, csvout, idcol):
    """Add random return_code column to a spreadsheet.

    Args:
        csvin: input file
        csvout: output file
        idcol (str): column name for ID number

    Returns:
        dict of the mapping from student number to secret code.
    """
    from plom import isValidStudentNumber

    df = pandas.read_csv(csvin, dtype="object")

    assert idcol in df.columns, 'CSV file missing "{}" column'.format(idcol)

    cols = ["StudentID", "StudentName"]
    print("extracting the following columns: " + str(cols))
    assert all(
        [c in df.columns for c in cols]
    ), "CSV file missing columns?  We need:\n  " + str(cols)
    df = df[cols]

    df.insert(2, "Return Code", "")
    sns = {}
    for i, row in df.iterrows():
        sn = str(row[idcol])
        # blanks, not ID'd yet for example
        if not sn == "nan":
            assert isValidStudentNumber(sn), "Invalid student ID"
            code = my_secret()
            df.loc[i, "Return Code"] = code
            sns[sn] = code

    df = df.dropna()  # no empty rows
    df.to_csv(csvout, index=False)
    return sns


def csv_add_salted_return_codes(csvin, csvout, saltstr, idcol):
    """Add return_code column to a spreadsheet by hashing ID number.

    You should think for yourself about the security implications
    of using this code.

    Args:
        csvin: input file
        csvout: output file
        saltstr (str): very salty
        idcol (str): column name for ID number

    Returns:
        dict of the mapping from student number to secret code.
    """
    from plom import isValidStudentNumber

    df = pandas.read_csv(csvin, dtype="object")

    assert idcol in df.columns, 'CSV file missing "{}" column'.format(idcol)

    df.insert(2, "Return Code", "")
    sns = {}
    for i, row in df.iterrows():
        sn = str(row[idcol])
        # blanks, not ID'd yet for example
        if not sn == "nan":
            assert isValidStudentNumber(sn), "Invalid student ID"
            code = my_hash(sn, saltstr)
            df.loc[i, "Return Code"] = code
            sns[sn] = code
    df.to_csv(csvout, index=False)
    return sns


def canvas_csv_add_return_codes(csvin, csvout, saltstr):
    """Adds or replaces the return codes to the canvas csv.

    Args:
        csvin (str): the name of the csv file to read in from canvas.
        csvout (str): the name of the output csv file when we are done.
        saltstr (str): the string to salt the student numbers.

    Raises:
        ValueError: if the canvas return code is present but not correct.

    Returns:
        dict : student number (str) -> hashed code.
    """
    print("*** Generating Return Codes Spreadsheet ***")
    df = import_canvas_csv(csvin)

    cols = ["Student", "ID", "SIS User ID", "SIS Login ID", "Section", "Student Number"]
    assert all(
        [c in df.columns for c in cols]
    ), "CSV file missing columns?  We need:\n  " + str(cols)

    rcode = find_partial_column_name(df, "Return Code (", at_start=False)
    cols.append(rcode)

    df = df[cols]

    sns = {}
    for i, row in df.iterrows():
        name = row["Student"]
        sn = str(row["SIS User ID"])
        sn_ = str(row["Student Number"])
        # as of 2019-10 we don't really dare use Student Number but let's ensure its not insane if it is there...
        if not sn_ == "nan":
            assert sn == sn_, (
                "Canvas has misleading student numbers: "
                + str((sn, sn_))
                + ", for row = "
                + str(row)
            )

        # TODO: UBC-specific student numbers
        assert len(name) > 0, "Student name is empty"
        assert len(sn) == 8, "Student number is not 8 characters: row = " + str(row)

        code = my_hash(sn, saltstr)

        oldcode = row[rcode]
        if pandas.isnull(oldcode):
            oldcode = ""
        else:
            oldcode = str(oldcode)
            # strip commas and trailing decimals added by canvas
            oldcode = oldcode.replace(",", "")
            # TODO: regex to remove all trailing zeros would be less fragile
            oldcode = oldcode.replace(".00", "")
            oldcode = oldcode.replace(".0", "")

        if oldcode == code:
            df.loc[i, rcode] = code  # write back as integer
            sns[sn] = code
            print(
                '  row {0}: already had (correct) code {1} for {2} "{3}"'.format(
                    i, oldcode, sn, name
                )
            )
        elif oldcode == "":
            df.loc[i, rcode] = code
            sns[sn] = code
            print('  row {0}: adding code {3} for {2} "{1}"'.format(i, name, sn, code))
        else:
            print(
                '  row {0}: oops sn {1} "{2}" already had code {3}'.format(
                    i, sn, name, oldcode
                )
            )
            print("    (We tried to assign new code {0})".format(code))
            print("    HAVE YOU CHANGED THE SALT SINCE LAST TEST?")
            raise ValueError("old return code has changed")
    df.to_csv(csvout, index=False)
    print('File for upload to Canvas: "{0}"'.format(csvout))
    return sns


def canvas_csv_check_pdf(sns):
    """Checks that each returned paper has a corresponding student number in the canvas files.

    Args:
        sns (): student number (str) -> hashed code.
    """
    print(
        "Checking that each codedReturn paper has a corresponding student in the canvas sheet..."
    )
    for file in os.scandir("codedReturn"):
        if file.name.endswith(".pdf"):
            # TODO: this looks rather fragile!
            parts = file.name.partition("_")[2].partition(".")[0]
            sn, meh, code = parts.partition("_")
            if sns.get(sn) == code:
                print(
                    "  Good: paper {2} has entry in spreadsheet {0}, {1}".format(
                        sn, code, file.name
                    )
                )
                sns.pop(sn)
            else:
                print(
                    "  ***************************************************************"
                )
                print(
                    "  Bad: we found a pdf file that has no student in the spreadsheet"
                )
                print("    Filename: {0}".format(file.name))
                print(
                    "  ***************************************************************"
                )
                # sys.exit()

    # anyone that has a pdf file has been popped from the dict, report the remainders
    if len(sns) == 0:
        print("Everyone listed in the canvas file has a pdf file")
    else:
        print(
            "The following people are in the spreadsheet but do not have a pdf file; did they write?"
        )
        for (sn, code) in sns.items():
            # TODO: name rank and serial number would be good
            print("  SN: {0}, code: {1}".format(sn, code))
