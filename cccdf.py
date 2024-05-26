


import json
import os
# dirs = [
#     ['CBR0429', 'CBR'],
#     ['VBV_3', 'Ours'],
#     ['VBV_5', 'Ours'],
#     ['VBV_10', 'Ours'] ,
#     ['CBR_factor_0.7', 'CBR'],
#     ['CBR_factor_0.9', 'CBR'],
#     ['CBR_factor_1.1', 'CBR'],
#     ['CBR_factor_1.3', 'CBR'],
#     ['Pacing', 'Pacing']
    
#         ]

dirs = ['CBR0429', 'VBV_10', 'CBR_factor_0.7', 'CBR_factor_0.9', 'CBR_factor_1.1', 'CBR_factor_1.3', 'Pacing','VP8']
category = ['CBR', 'Ours', 'CBR', 'CBR', 'CBR', 'CBR', 'WebRTC - x264', 'WebRTC - VP8','Salsify']
annotations = ['CBR 1.0', 'Ours', 'CBR 0.7', 'CBR 0.9', 'CBR 1.1', 'CBR 1.3', 'WebRTC - x264', 'WebRTC - VP8','Salsify']





psnr_data = []
latency_data = []
vmaf_data = []

for d in dirs:
    d = os.path.join("/home/xiangjie/Mahimahi-Test/archive/",d)
    ts = os.listdir(d)
    ts = sorted(ts)
    d = os.path.join(d, ts[-1])
    with open(os.path.join(d, 'quality_seq.json')) as f:
        quality_dict = json.load(f)
        psnr_data.append(quality_dict['psnr'])
        vmaf_data.append(quality_dict['vmaf'])
    with open(os.path.join(d, 'result.json')) as f:
        data = json.load(f)
        latency_data.append(data['latency'])
    
    
import json

# load salsifydelays.json
with open("salsifydelays.json") as f:
    sal_delays = json.load(f)

latency_data.append(sal_delays)

with open("salsify.json") as f:
    quality_dict = json.load(f)
    psnr_data.append(quality_dict['psnr'])
    vmaf_data.append(quality_dict['vmaf'])
    

import plotly.express as px


    
# cdf plotly
fig = px.line(title='CDF of PSNR')

for i, psnr in enumerate(psnr_data):
    print(psnr)
    psnr = [x for x in psnr if x is not None and x >0]
    psnr.sort()
    
    y = [(j + 1) / len(psnr) for j in range(len(psnr))]
    fig.add_scatter(x=psnr, y=y, mode='lines', name=annotations[i])

fig.write_html("cdf_psnr.html")

os.system("sudo cp cdf_psnr.html /var/www/html/t2/")


fig = px.line(title='CDF of Latency')

latency_percent = []

percent = 0.9
for i, delay in enumerate(latency_data):
    delay = [x for x in delay if x is not None]
    delay.sort()
    y = [(i + 1) / len(delay) for i in range(len(delay))]
    latency_percent.append(delay[int(len(delay) * percent)]) 
    fig.add_scatter(x=delay, y=y, mode='lines', name=annotations[i])

# fig.show()
# save html

fig.write_html("cdf_latency.html")
fig.write_image("cdf_latency.pdf")

os.system("sudo cp cdf_latency.html /var/www/html/t2/")

# tradeoff plotly
fig = px.scatter(x=latency_percent, y=vmaf_data, color=category, size_max=60)

# add annotation
for i in range(len(latency_percent)):
    fig.add_annotation(x=latency_percent[i], y=vmaf_data[i],
                        text=annotations[i],
                        showarrow=True,
                        arrowhead=1)


fig.update_layout(
    xaxis_title=f"{percent * 100}% percentile Latency (ms)",
    yaxis_title=f"VMAF Score",
)

# set image size
fig.update_layout(
    autosize=False,
    width=1200,
    height=550,
)

# set style to be science style
fig.update_layout(template="plotly_white")


# set font size
fig.update_layout(
    font=dict(
        family="Courier New, monospace",
        size=18,
        color="Black"
    )
)

# x axis reverse
fig.update_xaxes(autorange="reversed")



fig.update_traces(marker=dict(size=12,
                                line=dict(width=2,
                                            color='DarkSlateGrey')),
                    selector=dict(mode='markers'))


fig.write_html("tradeoff.html")

# save pdf

fig.write_image("tradeoff.pdf")
import time
time.sleep(0.5)
fig.write_image("tradeoff.pdf")

os.system("sudo cp tradeoff.html /var/www/html/t2/")
    
    

