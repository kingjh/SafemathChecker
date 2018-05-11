import os
from os.path import basename
import re
import shutil
from SafeMathXref import SafeMathXref
from OperatorParser import OperatorParser

SAFE_MATH_FILE_NAME = "SafeMath"
MATH_PATH = "math"
TO_CHECK_PATH = "." + os.sep + "to_check"
BACKUP_PATH = "." + os.sep + "backup"
MAX_TIMES = 32
BYTES = lambda x: str((x + 1) * 8) if x != MAX_TIMES - 1 else ""

safe_math_xrefs = list(range(0, MAX_TIMES))
# init SafeMath file names list, MAX_TIMES dimensions (8 to 256, step=8)
for i in range(0, MAX_TIMES):
    safe_math_xrefs[i] = SafeMathXref(MAX_TIMES)

# init sol file names list
non_safe_math_file_names = []


def match_file_name(root, file_name):
    full_path = root + os.sep + file_name
    if not re.match(r"\w+.sol", file_name):
        # if it's not a *.sol file, ignore
        return

    is_safe_math = False
    for i in range(0, MAX_TIMES):
        if file_name == SAFE_MATH_FILE_NAME + BYTES(i) + ".sol":
            # if it's a SafeMath*.sol file, record
            is_safe_math = True
            safe_math_xrefs[i].safe_math_file_name = full_path
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
    # delete backup files
    shutil.rmtree(BACKUP_PATH, ignore_errors=True)

    is_uint_used = [False] * MAX_TIMES
    for sol_file_name in non_safe_math_file_names:
        # backup *.sol files
        paths = sol_file_name.split(os.sep)
        backup_path = BACKUP_PATH + os.sep + os.sep.join(paths[2: -1]) + os.sep
        backup_file_name = backup_path + basename(sol_file_name).split(".")[0] + ".sol"
        if not os.path.exists(backup_path):
            os.makedirs(backup_path)

        shutil.move(sol_file_name, backup_file_name)
        rfp = open(backup_file_name, 'r', newline='')
        wfp = open(sol_file_name, 'w', newline='')
        rn = 0
        # contract row no
        crn = 1
        is_before_contract = True
        is_safe_math_imported = [False] * MAX_TIMES
        is_safe_math_used = [False] * MAX_TIMES
        new_lines = []
        for line in rfp.read().splitlines():
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
            new_lines.append(operator_parser.replace_operators(line))
            rn += 1

        d = 1
        for i in range(0, MAX_TIMES):
            if is_uint_used[i] and not is_safe_math_imported[i]:
                # import the missing SafeMath file
                new_lines.insert(crn - 1, "import " + "\"." + os.sep + MATH_PATH + os.sep + SAFE_MATH_FILE_NAME +
                                 BYTES(i) + ".sol\";")
                crn += 1

            if is_uint_used[i] and not is_safe_math_used[i]:
                # use missing SafeMath file
                new_lines.insert(crn + d, "    using " + SAFE_MATH_FILE_NAME + BYTES(i) + " for uint" +
                                 BYTES(i) + ";")
                d += 1

        wfp.write(os.linesep.join(new_lines))
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
            safe_math_xrefs[i].safe_math_file_name = "." + os.sep + MATH_PATH + os.sep + safe_math_file_name
            create_safe_math_file(safe_math_file_name, i)


def create_safe_math_file(safe_math_file_name, i):
    """ create SafeMath*.sol file """
    to_check_math_path = TO_CHECK_PATH + os.sep + MATH_PATH
    max_byte = 8 * MAX_TIMES
    rfp = open("." + os.sep + MATH_PATH + os.sep + SAFE_MATH_FILE_NAME + ".sol", 'r', newline='')
    try:
        os.makedirs(to_check_math_path)
    except FileExistsError:
        pass

    wfp = open(to_check_math_path + os.sep + safe_math_file_name, 'w', newline='')
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

    # for testing
    # line = "(v1+2)*3 >= v1"
    # operator_parser = OperatorParser()
    # print(line)
    # print(operator_parser.replace_operators(line))


