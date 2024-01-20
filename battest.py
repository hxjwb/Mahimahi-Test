


bws = [6]
qs = 1000

import os
import time

for bw in bws:
    cmd = f'python webrtc_test.py --bw {bw} --queue {qs}'
    os.system(cmd)
    # time.sleep(30)