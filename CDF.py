


def get_delays(file):
    lines = []
    with open(file) as f:
        lines = f.readlines()

    delays = []
    for line in lines:
        if "net_delay" in line:
            line = line.strip()
            print(line)
            net_delay = line.split('net_delay=')[1].split(',')[0]
            print(net_delay)
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


delays = get_delays('res/ours.log') # No pace and no action
delays2 = get_delays('res/pace.log') # No pace and action

# draw the graph
import matplotlib as mpl
mpl.use('Agg')

import matplotlib.pyplot as plt

# draw cdf of delays

delays.sort()
delays2.sort()

y = []
for i in range(len(delays)):
    y.append((i + 1) / len(delays))
    
y2 = []
for i in range(len(delays2)):
    y2.append((i + 1) / len(delays2))

plt.plot(delays, y, label='Ours',color='Coral')
plt.plot(delays2, y2, label='Pace',color='Black')

plt.xlabel('Delay (ms)')
plt.ylabel('CDF')
plt.legend()
# use percentage
plt.gca().yaxis.set_major_formatter(mpl.ticker.FuncFormatter(lambda y, _: '{:.0%}'.format(y)))
plt.title('CDF of Delays')

plt.savefig('delays.png')
plt.clf()

