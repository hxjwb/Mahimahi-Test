
bin_path = "/home/xiangjie/sparkrtc/out/t"
video_file = "/home/xiangjie/new.yuv"
w,h = 1920, 1080
fps = 10
# recon_file = "res/recon.yuv"
duration =  15 # seconds


import subprocess
import os
import time

def start_process(cmd, error_log_file=None, std_log_file=None):
    if error_log_file:
        with open(error_log_file, 'w') as f:
            return subprocess.Popen(cmd, shell=True,stdin=subprocess.PIPE, stderr=f, preexec_fn=os.setsid)
    else:
        return subprocess.Popen(cmd, shell=True,preexec_fn=os.setsid)

def kill_process(process):
    import signal
    process.terminate() 
    process.wait()
    os.killpg(process.pid,signal.SIGTERM)

# queue_size = 1
if __name__ == "__main__":
    
    # --bw 2 --queue 100
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--bw', type=str, default=6)
    parser.add_argument('--queue', type=int, default=80)
    parser.add_argument('--logsend', type=str, default='oksen')
    parser.add_argument('--logrecv', type=str, default='okre')
    parser.add_argument('--figname', type=str, default='figname')
    parser.add_argument('--recon', type=str, default='res/recon.yuv')
    args = parser.parse_args()
    bw = args.bw
    queue_size = args.queue
    logsend = args.logsend
    logrecv = args.logrecv
    figname = args.figname
    recon_file = args.recon
    # trace_up = f'traces/{bw}mbps.t'
    # trace_down = f'traces/{bw}mbps.t'
    tracefile = 'trace_1000427_http---www.msn.com-'
    trace_up = f'traces/{bw}mbps.t'
    trace_down = f'traces/{tracefile}'

    
    # end process that occupies the port 8888
    
    os.system("fuser -k 8888/tcp")

    # Start the server
    server_cmd = os.path.join(bin_path, 'peerconnection_server')
    server_process = start_process(server_cmd)

    # Start the clients
    cmd_sender = f"{bin_path}/peerconnection_localvideo --file {video_file} --width {w} --height {h} --fps {fps} --logname {logsend} "
    
    cmd_receiver = f"mm-link {trace_up} {trace_down} --downlink-log=logs/mah.log --downlink-queue=droptail --downlink-queue-args=packets={queue_size}"
    # cmd_receiver = "mm-lo dss downlink 0.1"
    # cmd_receiver = "mm-delay 1000"
    rec_process = start_process(cmd_receiver, 'logs/receiver.log')
    
    # input_line = f"ifconfig > ifconfig.txt\n" 
    # rec_process.stdin.write(input_line.encode())
    # rec_process.stdin.flush()
    
    input_line = f"{bin_path}/peerconnection_localvideo --recon {recon_file} --server 100.64.0.1 --logname {logrecv}\n" # 
    rec_process.stdin.write(input_line.encode())
    rec_process.stdin.flush()
    
    

    # # receiver first, wait for 200ms
    time.sleep(1)
    sen_process = start_process(cmd_sender, 'logs/sender.log')

    # wait for duration seconds
    time.sleep(duration)
    
    
    # kill the processes
    kill_process(sen_process)
    kill_process(rec_process)
    kill_process(server_process)

    print("Test Done!")
    
