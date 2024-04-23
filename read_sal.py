

sender_log = "s.txt"
receiver_log = "r.txt"


file = open(sender_log, "r")

lines = file.readlines()

file.close()


send_ts = [0 for i in range(1000)]
recv_ts = [0 for i in range(1000)]

for line in lines:
    if "framenum|timestamp" in line:
        values = line.split(" ")[1].strip().split("|")
        num, ts = values[0], values[1]
        num = int(num)
        ts = int(ts)
        send_ts[num] = ts
        

file = open(receiver_log, "r")

lines = file.readlines()

file.close()

for line in lines:
    if "framenum|nowtimestamp" in line:
        values = line.split(" ")[1].strip().split("|")
        num, ts = values[0], values[1]
        num = int(num)
        ts = int(ts)
        recv_ts[num] = ts
        
        
# get the delays

delays = [recv_ts[i] - send_ts[i] for i in range(1000)]


# if < 0, then -1
delays =   [d if d >= 0 else -1 for d in delays]

delays = [d for d in delays if d != 0]
print(delays)

# avg, 90th, 99th
delays = sorted(delays)
avg = sum(delays) / len(delays)
print(avg)
print(delays[int(len(delays) * 0.9)])
print(delays[int(len(delays) * 0.99)])


cmd = "python3 QRdec.py output.yuv -o salsify.json -r /home/xiangjie/Mahimahi-Test/video/gta6_30_coded.yuv "

import os
os.system(cmd)


cmd = "python3 cdf.py salsify.json -o salsify_psnr"

os.system(cmd)