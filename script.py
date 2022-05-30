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
        i_end = i_start + 6

        uuid = line[i_start:i_end]

        type = line[:i_start - 1]
        type = type.upper()
        type = '_'.join(type.split())
        type = re.sub("[^a-zA-Z]", "", type)

        for_ = line[i_end + 1:]
        for_ = for_.upper()
        for_ = '_'.join(for_.split())
        for_ = re.sub("[^a-zA-Z]", "", for_)

        bleuuid = BLEUUID(type, uuid, for_)
        uuids.append(bleuuid)
        print(f"{bleuuid.uuid} -> {bleuuid.for_} -> {bleuuid.type}")


def makedoth():
    with open('BLE_UUIDS.h', 'w', encoding="utf-8") as doth:
        for uuid in uuids:
            doth.writelines([f"#define {uuid.type}_{uuid.for_} {uuid.uuid}\n"])
        doth.close()

    with open('uuidbank.dart', 'w', encoding="utf-8") as dotdart:
        dotdart.writelines([
            '''
        // Use as such : 
        Guid({CONST VALUE});
         '''
        ])

        dotdart.writelines(['class UUIDBANK {'])

        for uuid in uuids:
            dotdart.writelines(
                [f"static const {uuid.type}_{uuid.for_} = {uuid.uuid};"])

        dotdart.writelines(['}'])


openfile()
removeheader()
removefooter()
extractinfo()
makedoth()
