MTU = 1500

# generate a trace file from bandwith

bw = 1.5 # Mbps

filename = f"traces/{bw}mbps.t"

f = open(filename, 'w')

# MTU / Interval = bw
interval = MTU * 8 / bw / 1000 

print("Interval: " + str(interval))

# fixed bandwidth
for i in range(20):
    # print(int(interval * i))
    f.write(f"{int(interval * i)}\n")

f.close()    
