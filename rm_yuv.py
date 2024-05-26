# 递归删除archive目录下的所有recon.yuv文件
#
import os

def remove_recon_yuv(path):
    if not os.path.exists(path):
        return
    if os.path.isfile(path):
        if path.endswith("recon.yuv"):
            os.remove(path)
    else:
        for file in os.listdir(path):
            remove_recon_yuv(os.path.join(path, file))
            
remove_recon_yuv("archive")


