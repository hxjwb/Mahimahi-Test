trace_up = "traces/12mbps.t"
trace_down = "traces/12mbps.t"
queue_size = 1001
import subprocess,os,time

def start_process(cmd, error_log_file=None, std_log_file=None):
    # if error_log_file:
    with open(error_log_file, 'w') as f:
        return subprocess.Popen(cmd, shell=True,stdin=subprocess.PIPE, stdout=f, preexec_fn=os.setsid)
    # else:
    #     return subprocess.Popen(cmd, shell=True,preexec_fn=os.setsid)

def kill_process(process):
    import signal
    process.terminate() 
    process.wait()
    os.killpg(process.pid,signal.SIGTERM)
        
if __name__ == "__main__":
    import argparse
    # url 
    parser = argparse.ArgumentParser()
    parser.add_argument('--url', type=str, default="http://www.google.com")
    url =  parser.parse_args().url
    
    cmd_mahi = f"mm-link {trace_up} {trace_down} --downlink-log=logs/testmah.log --downlink-queue=droptail --downlink-queue-args=packets={queue_size} > out.log 2> err.log"
    print(cmd_mahi)
    rec_process = start_process(cmd_mahi, 'logs/runsel1.log')


    time.sleep(1)
    input_line = f"python3 sel.py --url https://{url} > out.log 2> err.log &\n"
    rec_process.stdin.write(input_line.encode())
    rec_process.stdin.flush()


    print("run sel.py")

    time.sleep(30)
    kill_process(rec_process)


    logfile = 'logs/testmah.log'

    file = open(logfile, 'r')
    lines = file.readlines()
    file.close()


    x = []
    y = []
    for line in lines:
        if ' s ' in line:
            line = line.strip().split()
            
            # print(line)
            timestamp = line[0]
            timestamp = int(timestamp)
            if timestamp < 600000:
                x.append(timestamp)
                packets = line[2]
                packets = int(packets)
                # packets = 1000 - packets
                
                y.append(packets)
            
    import plotly.graph_objects as go

    # Create traces
    fig = go.Figure()

    fig.add_trace(go.Scatter(x=x, y=y,
                        mode='lines',
                        name='packets'))

    # rangeslider visible
    fig.update_layout(xaxis_rangeslider_visible=True)

    fig.update_layout(title='Packets',
                        xaxis_title='time',
                        yaxis_title='packets')

    fig.write_html(f"urls/{url}.html")
