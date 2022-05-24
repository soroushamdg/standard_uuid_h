from cgitb import text
import re
from uuid import UUID
# PROCCESS :
# 1 OPEN THE FILE
# 2 REMOVE HEADER
# 3 REMOVE PAGE NUMBERS
# 4 EXTRACT VARS FOR EACH ROW
# 5 WRITE NEW .H FILE


class BLEUUID:

    def __init__(self, type, uuid, for_):
        self.type = type
        self.uuid = uuid
        self.for_ = for_


uuids = []


def openfile():
    global text
    print("Opening file")
    with open('text.txt', 'r', encoding="utf8") as file:
        text = file.read()
    return text


def removeheader():
    global text
    index = text.find('Protocol Identifier')
    text = text[index:]


def removefooter():
    global text
    start = "Bluetooth SIG Proprietary"
    end = "Allocation type Allocated UUID Allocated for"
    occurs = text.count('Bluetooth SIG Proprietary')
    for _ in range(occurs):
        start_index = text.find(start)

        end_index = text.find(end) + len(end) + 1

        if (text.find(end) == -1):
            end_index = -1
            # +1 is for the last \n after r and other +1 to start from a char after that
        if (end_index != -1):
            text = text[:start_index] + text[end_index:]
        else:
            text = text[:start_index]


def extractinfo():
    global uuids
    global text
    text = text.splitlines()
    for line in text:
        i_start = line.find("0x")
        i_end = i_start + 5
        uuid = line[i_start:i_end]
        type = line[:i_start - 1 - 1]
        for_ = line[i_end + 1:]
        uuids.append(BLEUUID(type, uuid, for_))


openfile()
removeheader()
removefooter()
extractinfo()
# for i in uuids:
#     print(f"{i.uuid} : {i.type}")