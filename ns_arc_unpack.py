#!/usr/bin/python3
import sys
import json
import os

originPath = r'F:\NS-Unpack\NCA-NSP-XCI_TO_LayeredFS_v1.6\Updated_LayeredFS\romfs'
dumpPath = "dump"


def unpack(input_json, input_pack):
    with open(input_pack, 'rb') as arc_pack:
        with open(input_json, 'r') as arc_json:
            data = json.load(arc_json)
            for group in data["Groups"]:
                group_path = dumpPath + "/" + group["Name"]
                if not os.path.exists(group_path):
                    os.mkdir(group_path)
                for OrderedEntry in group["OrderedEntries"]:
                    file_path = group_path + "/" + OrderedEntry["OriginalFilename"]
                    if not os.path.exists(file_path[0:file_path.rfind("/")]):
                        os.makedirs(file_path[0:file_path.rfind("/")])
                    arc_pack.seek(OrderedEntry["Offset"])
                    with open(file_path, 'wb') as dumpFile:
                        dumpFile.write(arc_pack.read(OrderedEntry["Length"]))
                        dumpFile.close()
                    print("提取完毕：" + file_path)


if __name__ == '__main__':
    if not os.path.exists(dumpPath):
        os.mkdir(dumpPath)
    for root, dirs, files in os.walk(originPath):
        for file in files:
            path = os.path.join(root, file)
            if path.endswith('.json'):
                json_file = path
                pack_file = path.replace('.json', '.pack')
                unpack(json_file, pack_file)
