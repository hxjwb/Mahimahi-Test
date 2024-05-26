import json
with open("salsifydelays.json") as f:
    sal_delays = json.load(f)
    
new_sal_delays = []

for delay in sal_delays:
    new_sal_delays.append(delay + 10) # RTT

# dump new_sal_delays to salsifydelays.json
with open("salsifydelays.json", 'w') as f:
    json.dump(new_sal_delays, f)
    