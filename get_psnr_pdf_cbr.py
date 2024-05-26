



import os



def findthelatest(fileli):
    fileli.sort()
    return fileli[-1]

if __name__ == "__main__":
    # names_CBR = [f'auto_CBR{i}' for i in range(0, 7)]
    
    names = []
    category = []
    names.extend([f'auto_CBR_factor_{i/10}' for i in range(5, 16, 1)])
    category.extend(["CBR" for i in range(5, 16, 1)])
    
    # names.extend([f'test_fix_bitrate{i}' for i in [1,2,3,4,5,6,8]])
    # category.extend(["test" for i in [1,2,3,4,5,6,8]])
    
    # names.extend([f'auto_vbv_{i}' for i in [6]])
    # category.extend(["ours" for i in [4]])
    
    names.append('vp8')
    category.append('vp8')
    
    # names.extend([f'auto_CBR_factor_{i}' for i in [0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2,1.3, 1.4, 1.5]])
    # category.extend(["CBR" for i in [0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2,1.3, 1.4, 1.5]])
    
    
    result_files = []
    for i in names:
        name = i
        
        path = f"archive/{name}"
        
        fileli = os.listdir(path)
        filename = findthelatest(fileli)
        
        file_path = os.path.join(path, filename)
        file_path = os.path.join(file_path, "result.json")

        result_files.append(file_path)


    print(result_files)
    
    # cmd = f'python3 cdf.py {" ".join(result_files)}'
    # print(cmd)
    
    # os.system(cmd)

    delays = []
    psnrs = []
    framerates = []
    for file in result_files:
        # print(file)
        
        results =  []
        import json
        with open(file, 'r') as f:
            data = json.load(f)
            results.append(data)
            
        for result in results:
            # remove null
            result['psnr'] = [x if x is not None else 0 for x in result['psnr']]
            result['latency'] = [x  for x in result['latency'] if x is not None]
            delays.append(result['latency'])
            psnrs.append(result['psnr'])
            
            framerate = len(result['psnr'])/1600 * 30
            framerates.append(framerate)
            

            
            

    x = []
    y = []


    x_percentile = 0.9
    y_percentile = 0.5
    
    




    for i in range(len(delays)):
        
        p_x = delays[i][int(len(delays[i]) * x_percentile )]
        p_y = psnrs[i][int(len(psnrs[i]) * y_percentile )]
        average_x = sum(delays[i]) / len(delays[i])
        average_y = sum(psnrs[i]) / len(psnrs[i])

        x.append(p_x)
        y.append(p_y)
        
        

    import plotly.express as px

    fig = px.scatter(x=x, y=y, color=category, size_max=60)

    #
    for i in range(len(x)):
        fig.add_annotation(x=x[i], y=y[i],
                    text=names[i] + f' {framerates[i]:.1f}fps',
                    showarrow=True,
                    arrowhead=1)


    fig.update_layout(
        xaxis_title=f"Latency(ms){x_percentile * 100} percentile",
        yaxis_title=f"PSNR(dB) {y_percentile * 100} percentile",
    )

    # x axis reverse
    fig.update_xaxes(autorange="reversed")



    fig.update_traces(marker=dict(size=12,
                                    line=dict(width=2,
                                                color='DarkSlateGrey')),
                        selector=dict(mode='markers'))


    fig.show()
    
    fig_psnr_cdf = px.ecdf(psnrs, color=names)
    fig_psnr_cdf.write_html("psnr_cdf.html")
    
    fig_latency_cdf = px.ecdf(delays, color=names)
    fig_latency_cdf.write_html("latency_cdf.html")
    
    
    


        