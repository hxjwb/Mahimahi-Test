

import os
os.chdir('res')

fileli = os.listdir()

# sort the file list by queue size
fileli.sort(key=lambda x: int(x.split('_')[0]))

x = []
y = []
for file in fileli[:6]:
    if 'txt' in file:
        f = open(file, 'r')
        lines = f.readlines()
        f.close()
        qs = int(file.split('_')[0])
        x.append(qs)
        print(qs,end=' ')
        for line in lines:
            if 'delay' in line:
                ave_delay = float(line.strip().split()[-1]) 
                y.append(ave_delay)
                print(ave_delay)
                
                
import matplotlib.pyplot as plt
plt.plot(x,y)
plt.xlabel('Queue Size')
plt.ylabel('Average Delay (ms)')
plt.title('Average Delay vs Queue Size')

plt.savefig('../image/delay100.png')