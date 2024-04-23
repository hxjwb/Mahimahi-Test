



video_file = "/home/xiangjie/Mahimahi-Test/video/tl_1000.mp4"

output_file = "/home/xiangjie/Mahimahi-Test/video/gta6.yuv"

# to yuv420

cmd = f"ffmpeg -i {video_file} -c:v rawvideo -pix_fmt yuv420p {output_file}"

import os
os.system(cmd)

