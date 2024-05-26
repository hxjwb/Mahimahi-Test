

from matplotlib import pyplot as plt
import scienceplots

import matplotlib as mpl
mpl.use('Agg')


# use science style


mpl.style.use(['science', 'ieee',  'no-latex'])

# 1. Showing latency cdf 

# font size

plt.rcParams.update({'font.size': 10})

js = "/home/xiangjie/Mahimahi-Test/archive/Pacing/2024-04-30-19-59-47/result.json"
import json
data = json.load(open(js))
latency = data["latency"]
latency = [i for i in latency if i is not None]


latency.sort()


latency2 = [i * 0.5 for i in latency]

percentile = [i/len(latency) for i in range(len(latency))]
percentile2 = [i/len(latency2) for i in range(len(latency2))]



# figure size 

# plt.figure(figsize=(5, 5))

plt.plot(latency, percentile, label="End to end latency")
plt.plot(latency2, percentile2, label="Pacing latency")


plt.legend()
plt.xlabel("Latency (ms)")
plt.ylabel("CDF")

plt.savefig("cdf2.png")

# save pdf

plt.savefig("cdf2.pdf")



# motivation2 

#x: FPS
# y: latency

x = [0.5, 1, 5, 10, 20, 30, 60]

y_pacing = [100, 50, 25, 20, 15, 13, 10]

y_no_pacing = [150, 100,43, 32, 22, 18, 15]


drop_pacing = [0.1, 0.05, 0.02, 0.01, 0.005, 0.003, 0.001]
drop_no_pacing = [0.2, 0.1, 0.05, 0.03, 0.01, 0.005, 0.002]


plt.figure()

plt.plot(x, y_pacing, label="Pacing")

plt.plot(x, y_no_pacing, label="No pacing")

plt.xlabel("FPS")

plt.ylabel("Latency (ms)")

plt.legend()

plt.savefig("motivation21.pdf")

plt.figure()

plt.plot(x, drop_pacing, label="Pacing")

plt.plot(x, drop_no_pacing, label="No pacing")

plt.xlabel("FPS")

plt.ylabel("Packet drop rate")

plt.legend()

plt.savefig("motivation22.pdf")