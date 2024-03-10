



video_file = "/home/xiangjie/Mahimahi-Test/video/gta6trailer_1080.m4s"

output_file = "/home/xiangjie/Mahimahi-Test/video/gta6trailer_1080_60.yuv"

# to yuv420

cmd = f"ffmpeg -i {video_file} -c:v rawvideo -pix_fmt yuv420p {output_file}"

import os
os.system(cmd)

