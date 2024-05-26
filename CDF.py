


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
            else:
                net_delay = 9999
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

# delays = get_delays('res/pace.log') # Pace
import os

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--log1', type=str, default='res/ours.log')
    parser.add_argument('--label1', type=str, default='Ours')
    
    parser.add_argument('--log2', type=str, default='res/pace.log')
    parser.add_argument('--label2', type=str, default='Pace')
    
    parser.add_argument('--figname', type=str, default='delay_cdf.png')

    args = parser.parse_args()
    
    log1 = args.log1
    log2 = args.log2
    
    label1 = args.label1
    label2 = args.label2
    
    figname = args.figname  
    
    # get the delays
    delays = get_delays(log1) 
    delays2 = get_delays(log2) 

    # draw the graph
    import matplotlib as mpl
    mpl.use('Agg')

    import matplotlib.pyplot as plt

    # draw cdf of delays

    delays.sort()
    delays2.sort()
    
    # remove "9999" in delays
    delays = delays[:-2]
    delays2 = delays2[:-2]

    # get average, mid
    average1 = sum(delays) / len(delays)
    average2 = sum(delays2) / len(delays2)
    
    mid1 = delays[int(len(delays) / 2)]
    mid2 = delays2[int(len(delays2) / 2)]
    
    # print average, mid
    print(f'{label1} average delay: {average1:.2f}')
    print(f'{label2} average delay: {average2:.2f}')
    print(f'{label1} mid delay: {mid1:.2f}')
    print(f'{label2} mid delay: {mid2:.2f}')
    
    print() 
    
    y = []
    for i in range(len(delays)):
        y.append((i + 1) / len(delays))
        
    y2 = []
    for i in range(len(delays2)):
        y2.append((i + 1) / len(delays2))
        


    plt.plot(delays, y, label=label1,color='Coral')
    plt.plot(delays2, y2, label=label2,color='Black')

    plt.xlabel('Delay (ms)')
    plt.ylabel('CDF')
    plt.legend()
    # use percentage
    plt.gca().yaxis.set_major_formatter(mpl.ticker.FuncFormatter(lambda y, _: '{:.0%}'.format(y)))
    plt.title('CDF of Delays')

    plt.savefig(figname)
    plt.clf()
    
    
    cmd = "python3 compare_quality.py"
    os.system(cmd)

