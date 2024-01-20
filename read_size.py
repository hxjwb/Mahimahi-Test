

file = 'res.log'

sizes = []
with open(file) as f:
    lines = f.readlines()
    
    for line in lines:
        if 'Frame: size=' in line:
            print(line.split(',')[0].split('=')[1])
            size = int(line.split(',')[0].split('=')[1])
            sizes.append(size)
    
print(sizes)

# average
print(sum(sizes)/len(sizes))