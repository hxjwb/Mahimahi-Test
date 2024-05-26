

def get_CDF(name, values, labels):
    
    for i in range(len(values)):
        values[i] = [v for v in values[i] if v != None and 20 < v < 50]
    for l in values:
        l.sort()
    
        
    # draw cdf
    import matplotlib as mpl
    mpl.use('Agg')
    
    import matplotlib.pyplot as plt
    
    # 1/4 A4 width
    plt.figure(figsize=(8.3, 5.8))
    
    # font size 20
    plt.rc('font', size=20)
    
    ys = []
    for j in range(len(values)):
        y = [i/len(values[j]) for i in range(len(values[j]))]
        ys.append(y)
    
        
    for i in range(len(values)):
        plt.plot(values[i], ys[i], label=labels[i], linewidth=3)
        
    plt.legend()
    
    # grid
    plt.grid()
    
    plt.xlabel(name)
    
    plt.ylabel('CDF')
    
    plt.savefig(f'{name}_cdf.png')
    
    # save as pdf   
    plt.savefig(f'{name}_cdf.pdf')
    
    
    # print average,mid, 10th, 1th
    
    for i in range(len(values)):
        average = sum(values[i]) / len(values[i])
        mid = values[i][int(len(values[i]) / 2)]
        ten = values[i][int(len(values[i]) / 10)]
        one = values[i][int(len(values[i]) / 100)]
        
        print(f'{labels[i]} average {name}: {average:.2f}')
        print(f'{labels[i]} mid {name}: {mid:.2f}')
        print(f'{labels[i]} 10th {name}: {ten:.2f}')
        print(f'{labels[i]} 1th {name}: {one:.2f}')
        
    
    
    





import os

# cmd1 = "python3 QRdec.py /home/xiangjie/Mahimahi-Test/res/ours.yuv -o ours.json -r /home/xiangjie/Mahimahi-Test/video/gta6_30_coded.yuv -v /home/xiangjie/Mahimahi-Test/res/ours_vmaf.yuv"

# cmd2 = "python3 QRdec.py /home/xiangjie/Mahimahi-Test/res/pace.yuv -o pace.json -r /home/xiangjie/Mahimahi-Test/video/gta6_30_coded.yuv -v /home/xiangjie/Mahimahi-Test/res/pace_vmaf.yuv"

# os.system(cmd1)

# os.system(cmd2)


if __name__ == '__main__':
    
    # parse args 
    import argparse
    parser = argparse.ArgumentParser()
    # args are the json files
    parser.add_argument('files', type=str, nargs='+', help='json files')
    parser.add_argument('-o', type=str, default='psnr', help='name of the metric')
    args = parser.parse_args()
    
    jsons = args.files
    name = args.o
    import json
    
    psnrs = []
    
    # ssims = []
    
    labels = []
    for j in jsons:
        labels.append(j.split('/')[1])
    
    for j in jsons:
        with open(j, 'r') as f:
            data = json.load(f)
            
            psnrs.append(data['psnr'][4:])
            # ssims.append(data['ssim'])
            
    get_CDF(name, psnrs, labels)


