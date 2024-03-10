


input_yuv = "/home/xiangjie/Mahimahi-Test/video/gta6trailer_1080_60.yuv"

input_fps = 60

output_yuv = "/home/xiangjie/Mahimahi-Test/video/gta6trailer_1080_10.yuv"

output_fps = 10

file = open(input_yuv, "rb")

yuv = file.read()

file.close()

# get yuv into frames
import numpy as np

yuv = np.frombuffer(yuv, dtype=np.uint8)

yuv = yuv.reshape(-1, 1080*1920*3//2)

print(yuv.shape)

# change fps
import math

frame_interval = math.ceil(input_fps / output_fps)

print(frame_interval)

yuv = yuv[::frame_interval]

print(yuv.shape)

# save yuv
yuv = yuv.tobytes()

file = open(output_yuv, "wb")

file.write(yuv)

file.close()

