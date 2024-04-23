def get_CDF(name,l1,lable1,l2,lable2):
    
    # draw cdf
    import matplotlib as mpl
    mpl.use('Agg')

    import matplotlib.pyplot as plt

    plt.figure()
    l1.sort()

    y1 = [i/len(l1) for i in range(len(l1))]

    l2.sort()

    y2 = [i/len(l2) for i in range(len(l2))]


    plt.plot(l1, y1, label=lable1)
    plt.plot(l2, y2, label=lable2)

    plt.legend()

    plt.xlabel(name)

    plt.ylabel('CDF')

    plt.savefig(f'{name}_cdf.png')

    # print average,mid, 10th, 1th

    average1 = sum(l1) / len(l1)
    average2 = sum(l2) / len(l2)

    mid1 = l1[int(len(l1) / 2)]
    mid2 = l2[int(len(l2) / 2)]

    ten1 = l1[int(len(l1) / 10)]
    ten2 = l2[int(len(l2) / 10)]
    
    one1 = l1[int(len(l1) / 100)]
    one2 = l2[int(len(l2) / 100)]
    
    print(f'{lable1} average {name}: {average1:.2f}')
    print(f'{lable2} average {name}: {average2:.2f}')
    print(f'{lable1} mid {name}: {mid1:.2f}')
    print(f'{lable2} mid {name}: {mid2:.2f}')
    print(f'{lable1} 10th {name}: {ten1:.2f}')
    print(f'{lable2} 10th {name}: {ten2:.2f}')
    print(f'{lable1} 1th {name}: {one1:.2f}')
    print(f'{lable2} 1th {name}: {one2:.2f}')
    
    # plt.legend()
    
    # plt.savefig(f'{name}_cdf_with_lines.png')

import os

# cmd1 = "python3 QRdec.py /home/xiangjie/Mahimahi-Test/res/ours.yuv -o ours.json -r /home/xiangjie/Mahimahi-Test/video/gta6_30_coded.yuv -v /home/xiangjie/Mahimahi-Test/res/ours_vmaf.yuv"

# cmd2 = "python3 QRdec.py /home/xiangjie/Mahimahi-Test/res/pace.yuv -o pace.json -r /home/xiangjie/Mahimahi-Test/video/gta6_30_coded.yuv -v /home/xiangjie/Mahimahi-Test/res/pace_vmaf.yuv"

# os.system(cmd1)

# os.system(cmd2)

import json

with open('res/ours.json', 'r') as f:
    ours = json.load(f)

with open('res/pace.json', 'r') as f:
    pace = json.load(f)

ours_psnr = ours['psnr'][4:]
pace_psnr = pace['psnr'][4:]

ours_ssim = ours['ssim']
pace_ssim = pace['ssim']

get_CDF('psnr', ours_psnr, 'ours', pace_psnr, 'pace')

# get_CDF('ssim', ours_ssim, 'ours', pace_ssim, 'pace')

# calculate vmaf by ffmpeg
# file1 = "/home/xiangjie/Mahimahi-Test/res/ours.yuv"
# file2 = "/home/xiangjie/Mahimahi-Test/res/ours_vmaf.yuv"
# cmd = f"ffmpeg -hide_banner -video_size 416x240 -pixel_format yuv420p -i {file1} -video_size 416x240 -pixel_format yuv420p -i {file2} -lavfi ssim -f null -"

# os.system(cmd)

# file1 = "/home/xiangjie/Mahimahi-Test/res/pace.yuv"
# file2 = "/home/xiangjie/Mahimahi-Test/res/pace_vmaf.yuv"
# cmd = f"ffmpeg -hide_banner -video_size 416x240 -pixel_format yuv420p -i {file1} -video_size 416x240 -pixel_format yuv420p -i {file2} -lavfi ssim -f null -"

# os.system(cmd)




