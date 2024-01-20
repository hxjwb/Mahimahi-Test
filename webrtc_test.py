
bin_path = "/home/jiee/sparkrtc/out/t/"
video_file = "/home/jiee/ParkScene_1920x1080_24.yuv"
w,h = 1920, 1080
fps = 24
recon_file = "recon.yuv"
duration =  25 # seconds

# bw = 2 # Mbps

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
    parser.add_argument('--bw', type=str, default=2)
    parser.add_argument('--queue', type=int, default=100)
    args = parser.parse_args()
    bw = args.bw
    queue_size = args.queue
    trace_up = f'traces/{bw}mbps.t'
    trace_down = f'traces/{bw}mbps.t'
    
    # end process that occupies the port 8888
    
    os.system("fuser -k 8888/tcp")

    # Start the server
    server_cmd = os.path.join(bin_path, 'peerconnection_server')
    server_process = start_process(server_cmd)

    # Start the clients
    cmd_sender = f"{bin_path}/peerconnection_localvideo --file {video_file} --width {w} --height {h} --fps {fps} --logname send_{queue_size}_{bw} "
    
    cmd_receiver = f"mm-link {trace_up} {trace_down} --meter-downlink --meter-downlink-delay --downlink-queue=droptail --downlink-queue-args=packets={queue_size}"
    # cmd_receiver = "mm-loss downlink 0.2"
    # cmd_receiver = "mm-delay 1000"
    rec_process = start_process(cmd_receiver, 'logs/receiver.log')
    
    
    input_line = f"{bin_path}/peerconnection_localvideo --recon {recon_file} --server 100.64.0.5 --logname recv_{queue_size}_{bw}\n" # 100.64.0.5 is mahimahi IP
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

    print("Done!")
    
    # analyze the logs
    cmd = f"python log_reader.py res/{queue_size}_{bw}.txt"
    os.system(cmd)