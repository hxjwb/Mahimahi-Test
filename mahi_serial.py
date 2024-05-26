

# date = '2024-05-20-09-39-58'
# logfile = f'/home/xiangjie/Mahimahi-Test/archive/test_network/{date}/mah.log'


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='get the plot of the log file')
    parser.add_argument('path', type=str, help='path to log file')
    
    import os
    logpath = parser.parse_args().path
    logfile = os.path.join(logpath, 'mah.log')
    
    logsend = os.path.join(logpath, 'log_send_0')
    
    
    
    file = open(logfile, 'r')
    lines = file.readlines()
    file.close()
    
    file = open(logsend, 'r')
    send_lines = file.readlines()
    file.close()
    
    pid_list = []
    for line in send_lines:
        if 'PacketID' in line:
            line = line.strip().split()
            pid = line[-2]
            pid = int(pid)
            pid_list.append(pid)



    x = []
    y = []

    dic_packets = {}
    
    dic_frames = {}
    
    dic_drop = {}
    for line in lines:
        # if ' # ' in line:
    
        if ' s ' in line:
            line = line.strip().split()
            
            # print(line)
            timestamp = line[0]
            timestamp = int(timestamp)
            # if timestamp < 600000:
            x.append(timestamp)
            packets = line[2]
            packets = int(packets)
            # packets = 500 - packets
            
            y.append(packets)
        if ' + ' in line:
            timestamp,_,size,pid = line.strip().split()
            timestamp = int(timestamp)
            # if timestamp == 4900:
            #     print(line)
            size = int(size)
            pid = int(pid)
            
            if pid not in pid_list:
                continue
            
            if pid not in dic_frames:
               
                dic_frames[pid] = [timestamp]
            else:
                if timestamp not in dic_frames[pid]:
                    dic_frames[pid].append(timestamp)
            
            
            if timestamp not in dic_packets:
                dic_packets[timestamp] = size
            else:
                dic_packets[timestamp] += size
        if ' d ' in line:
            timestamp,_,_,_,pid = line.strip().split()
            timestamp = int(timestamp)
            pid = int(pid)
            if pid not in pid_list:
                continue
            
            if timestamp not in dic_drop:
                dic_drop[timestamp] = 1
            else:
                dic_drop[timestamp] += 1
    
    

    
    # print(dic_packets)
    x2 = [] # first timestamp of each frame
    y2 = [] # packet number
    for pid in dic_frames:
        timestamps = dic_frames[pid]
        total_packets = [ dic_packets[timestamp] for timestamp in timestamps]
        x2.append(timestamps[0])
        y2.append(sum(total_packets)/1500)
    
    
    # for i in range(len(x2)):
    #     print(x2[i], y2[i])
        
        
    # x2 = dic_packets.keys()
    # y2 = dic_packets.values()
        
    # x2 = list(x2)
    # y2 = list(y2)
            
    x3 = dic_drop.keys()
    y3 = dic_drop.values()
    
    x3 = list(x3)
    y3 = list(y3)
    
        
    import plotly.graph_objects as go

    # Create traces
    fig = go.Figure()

    fig.add_trace(go.Scatter(x=x, y=y,
                        mode='lines',
                        name='Queueing Packets'))

    # bar x2 y2
    fig.add_trace(go.Bar(x=x2, y=y2, name='Frame Packets'))


    # scatter x3 y3
    fig.add_trace(go.Scatter(x=x3, y=y3,
                        mode='lines',
                        name='Dropped Packets',
                        marker=dict(
                            size=10,
                            color='red',
                            symbol='x'
                        )))
    
    # y range 0-1000
    # fig.update_yaxes(range=[0, 1000])
    # rangeslider visible
    fig.update_layout(xaxis_rangeslider_visible=True)

    fig.update_layout(title='Packets',
                        xaxis_title='time',
                        yaxis_title='packets')

    fig.write_html( os.path.join(logpath, 'timeline.html'))
    
    fig.write_html( 'view/timeline.html')
    
    os.system("git commit -am 'update'")
    os.system("git push")
    
    

    



    
            
            
            