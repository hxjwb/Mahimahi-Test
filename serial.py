

# 绘制时序图，用plotly

input_json = "/home/xiangjie/Mahimahi-Test/archive/ours/2024-04-25-02-08-05/result.json"



if __name__ == '__main__':

    import json
    import os
    
    import argparse
    
    parser = argparse.ArgumentParser(description='get the plot of the result.json file')
    parser.add_argument('input_dir', type=str, help='path to input json file')
    
    
    input_dir = parser.parse_args().input_dir
    input_json = os.path.join(input_dir, 'result.json')
    


    with open(input_json, 'r') as f:
        data = json.load(f)
        
    size = data['size'] # frame size per frame id
    # if None in size, change it to 0
    size = [0 if x is None else int(x) for x in size]

    psnr = data['psnr']
    
    psnr_x = [i for i in range(len(psnr)) if psnr[i] is not None]
    psnr = [x for x in psnr if x is not None]

    # if None in psnr, change it to 0
    # psnr = [0 if x is None else x for x in psnr]
    latency = data['latency']
    latency_x = [i for i in range(len(latency)) if latency[i] is not None]
    latency = [x for x in latency if x is not None]

    
    
    fps = data['fps']
    fps_x = [i for i in range(len(fps)) if fps[i] is not None]
    fps = [x for x in fps if x is not None]

    encoding_bitrate = data['encoding_bitrate']

    fps_average = sum(fps) / len(fps)
    
    bwe = data['bwe']
    bwe_x = [i for i in range(len(bwe)) if bwe[i] is not None]
    bwe = [x/ 8 /fps_average  for x in bwe if x is not None]
    
    print("fps average: ", fps_average)
 


    import plotly.graph_objects as go
    from plotly.subplots import make_subplots

    # 柱形图sizes
    trace_sizes = go.Bar(
        x = list(range(len(size))),
        y = size,
        name = 'size',
        marker = dict(color = 'rgb(0, 255, 0)'),
        yaxis = 'y',
    )

    trace_bwe = go.Scatter(
        x = bwe_x,
        y = bwe,
        mode = 'lines',
        name = 'bwe',
        line = dict(color = 'rgb(255, 0, 0)'),
        yaxis = 'y'
    )
        

    # psnr
    trace_psnr = go.Scatter(
        x = psnr_x,
        y = psnr,
        mode = 'lines',
        name = 'psnr',
        line = dict(color = 'rgb(0, 0, 255)'),
        yaxis = 'y3'
    )

    # latency
    trace_latency = go.Scatter(
        x = latency_x,
        y = latency,
        mode = 'lines',
        name = 'latency',
        line = dict(color = 'rgb(0, 0, 0)'),
        yaxis = 'y2'
    )

    # data = [trace1, trace2, trace3]


    fig = make_subplots(rows=2,cols=1,
                        shared_xaxes=True,
                        specs=[[{"secondary_y": True}],[{"secondary_y": False}]]
                        )


    fig.add_trace(trace_sizes, row=1, col=1)
    fig.add_trace(trace_bwe, row=1, col=1)
    fig.add_trace(trace_latency, row=1, col=1, secondary_y=True)
    fig.add_trace(trace_psnr, row=2, col=1)


    fig.layout.xaxis2.rangeslider.thickness=0.05



    # fig['layout']['xaxis'].update(title='frame id')
    fig['layout']['xaxis2'].update(title='frame id')
    # fig['layout']['xaxis3'].update(title='frame id')


    fig['layout']['yaxis'].update(title='Size(bytes)', range=[0, 30000])
    fig['layout']['yaxis2'].update(title='latency(ms)')
    fig['layout']['yaxis3'].update(title='psnr')


    # fig.update_layout(height=800, width=800, title_text="subplots")

    # 设置 sub plots之间的间距


    # fig = go.Figure(data = data, layout = layout)
    fig.update_xaxes()
    # fig.show()

    fig.write_html(os.path.join(input_dir, 'serial.html'))
    # fig.show()



