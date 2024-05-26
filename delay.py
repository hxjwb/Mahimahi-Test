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
def get_delays(file):
    lines = []
    with open(file) as f:
        lines = f.readlines()

    delays = []
    for line in lines:
        if "net_delay" in line:
            line = line.strip()
            # print(line)
            net_delay = line.split('net_delay=')[1].split(',')[0]
            # print(net_delay)
            if net_delay != "None":
                net_delay = int(net_delay)

                delays.append(net_delay)

    # remove 9999 from the end
    index = len(delays) - 1
    while index >= 0:
        if delays[index] == 9999:
            delays.pop(index)
        else:  
            break
        index -= 1

    return delays
def get_CDF(name, values, labels):
    
    for l in values:
        l.sort()
    
    # draw cdf
    import matplotlib as mpl
    mpl.use('Agg')
    
    import matplotlib.pyplot as plt
    
        
    # 1/4 A4 width
    plt.figure(figsize=(8.3, 6.3))
    
    # font size 20
    plt.rc('font', size=20)
    ys = []
    for j in range(len(values)):
        y = [i/len(values[j]) for i in range(len(values[j]))]
        ys.append(y)
    
        
    for i in range(len(values)):
        plt.plot(values[i], ys[i], label=labels[i], linewidth=3)
        
    plt.grid()
    plt.legend()
    
    plt.xlabel(name)
    
    plt.ylabel('CDF')
    
    plt.savefig(f'{name}_cdf.png')
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
        
    
    
    





from cProfile import label
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
    parser.add_argument('-o', type=str, default='delay', help='name of the metric')
    args = parser.parse_args()
    
    logs = args.files
    name = args.o

    delays = []
    
    labels = []
    for log in logs:
        delays.append(get_delays(log))
        # get the file name without the path
        labels.append(log.split('/')[-1].split('.')[0])
                    
                    
            
    get_CDF(name, delays, labels)


