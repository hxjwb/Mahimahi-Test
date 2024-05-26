

path = "/home/xiangjie/Mahimahi-Test/archive/test_fix_bitrate8/2024-04-25-11-28-53"

import os

import json

# read json file

input_json = os.path.join(path, 'result.json')

with open(input_json, 'r') as f:
    data = json.load(f)
    