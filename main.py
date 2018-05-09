import os
from os.path import basename
import re
import shutil
from SafeMathXref import SafeMathXref
from OperatorParser import OperatorParser

# import "./SafeMath16.sol";
# using SafeMath16 for uint16;
SAFE_MATH_FILE_NAME = "SafeMath"
MATH_PATH = "math"
TO_CHECK_PATH = "./to_check"
BK_PATH = "./bk"
MAX_TIMES = 32
BYTES = lambda x: str((x + 1) * 8) if x != MAX_TIMES - 1 else ""

safe_math_xrefs = list(range(0, MAX_TIMES))
# init SafeMath file names list, MAX_TIMES dimensions (8 to 256, step=8)
for i in range(0, MAX_TIMES):
    safe_math_xrefs[i] = SafeMathXref(MAX_TIMES)

# init sol file names list
non_safe_math_file_names = []


def match_file_name(root, file_name):
    full_path = root + "/" + file_name
    if not re.match(r"\w+.sol", file_name):
        # if it's not a *.sol file, ignore
        return

    is_safe_math = False
    for i in range(0, MAX_TIMES):
        if file_name == SAFE_MATH_FILE_NAME + BYTES(i) + ".sol":
            # if it's a SafeMath*.sol file, record
            is_safe_math = True
            safe_math_xrefs[i].safe_math_file_name = "./" + MATH_PATH + "/" + file_name
            break

    # if it's a non SafeMath *.sol file, record
    if not is_safe_math:
        non_safe_math_file_names.append(full_path)


def search_safe_math_files():
    """ find and record the sol files' locations """
    for root, dirs, files in os.walk(TO_CHECK_PATH, topdown=False):
        for file_name in files:
            match_file_name(root, file_name)


def parse_sol_files():
    """ parse *.sol files """
    is_uint_used = [False] * MAX_TIMES
    for sol_file_name in non_safe_math_file_names:
        # backup *.sol files
        paths = sol_file_name.split('/')
        bk_path = BK_PATH + "/".join(paths[2: -1]) + "/"
        bk_file_name = bk_path + basename(sol_file_name).split(".")[0] + "_bk.sol"
        if not os.path.exists(bk_path):
            os.makedirs(bk_path)

        shutil.move(sol_file_name, bk_file_name)
        rfp = open(bk_file_name, 'r')
        wfp = open(sol_file_name, 'w', newline="\n")
        rn = 0
        # contract row no
        crn = 1
        is_before_contract = True
        is_safe_math_imported = [False] * MAX_TIMES
        is_safe_math_used = [False] * MAX_TIMES
        new_lines = []
        for line in rfp.readlines():
            if is_before_contract:
                if re.match(r".*contract *.", line):
                    # the row count of "contract..."
                    is_before_contract = False
                    crn = rn
                else:
                    for i in range(0, MAX_TIMES):
                        # find import
                        if re.match(r'.*import .*SafeMath' + BYTES(i) + '.sol[ "]*;', line):
                            is_safe_math_imported[i] = True
                            break
            else:
                for i in range(0, MAX_TIMES):
                    # find using statements and all uint usages
                    if re.match(r".*using .*SafeMath" + BYTES(i) + "[ ]*for[ ]*uint" + BYTES(i) + ";[ ]*", line):
                        is_safe_math_used[i] = True
                        break

                    if re.match(r".*[(]*uint" + BYTES(i) + " .*", line):
                        safe_math_xrefs[i].is_uint_used = True
                        is_uint_used[i] = True
                        break

            operator_parser = OperatorParser()
            # handle indent
            indent = len(line) - len(line.lstrip())
            leading_spaces = line[: indent]
            new_lines.append(leading_spaces + operator_parser.replace_operators(line[indent:]))
            rn += 1

        for i in range(0, MAX_TIMES):
            if is_uint_used[i] and not is_safe_math_imported[i]:
                # import the missing SafeMath file
                new_lines.insert(crn - 1, "import " + "\"./" + MATH_PATH + "/" + SAFE_MATH_FILE_NAME +
                                 BYTES(i) + ".sol\";" + os.linesep)
                crn += 1

            if is_uint_used[i] and not is_safe_math_used[i]:
                # use missing SafeMath file
                new_lines.insert(crn + 1, "    using " + SAFE_MATH_FILE_NAME + BYTES(i) + " for uint" +
                                 BYTES(i) + ";" + os.linesep)

        wfp.writelines(new_lines)
        wfp.flush()
        wfp.close()


def create_missing_safe_math_files():
    """ find if any uint type is used without corresponding SafeMath*.sol files, create the missing SafeMath*.sol
    files """
    for i in range(0, MAX_TIMES):
        if (safe_math_xrefs[i].safe_math_file_name == "") and safe_math_xrefs[i].is_uint_used:
            # there are *.sol files use a type of uint, but there are no corresponding SafeMath*.sol file
            # create the corresponding SafeMath*.sol file
            safe_math_file_name = SAFE_MATH_FILE_NAME + BYTES(i) + ".sol"
            safe_math_xrefs[i].safe_math_file_name = "./" + MATH_PATH + "/" + safe_math_file_name
            create_safe_math_file(safe_math_file_name, i)


def create_safe_math_file(safe_math_file_name, i):
    """ create SafeMath*.sol file """
    to_check_math_path = TO_CHECK_PATH + "/" + MATH_PATH
    max_byte = 8 * MAX_TIMES
    rfp = open("./" + MATH_PATH + "/" + SAFE_MATH_FILE_NAME + ".sol", 'r')
    try:
        os.makedirs(to_check_math_path)
    except FileExistsError:
        pass

    wfp = open(to_check_math_path + "/" + safe_math_file_name, 'w', newline="\n")
    generate_lines = lambda x: [re.sub(str(max_byte), BYTES(i), line) for line in x.readlines()]
    lines = generate_lines(rfp)
    wfp.writelines(lines)
    wfp.flush()
    wfp.close()
    rfp.close()


if __name__ == "__main__":
    # find and record the sol files' locations
    search_safe_math_files()

    # find all uint usages in *.sol files
    parse_sol_files()

    # create the missing SafeMath*.sol files
    create_missing_safe_math_files()
