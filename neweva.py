import argparse
import os
import json
if __name__ == "__main__":
    
    config_file = "config.json"
    import json
    with open(config_file) as f:
        config_dict = json.load(f)
        print(config_dict)
    
    parser = argparse.ArgumentParser()
    # parser.add_argument("-s", help="sender log file", default="/home/xiangjie/Mahimahi-Test/logs/np_pace_0")
    # parser.add_argument("-r", help="receiver log file", default="/home/xiangjie/Mahimahi-Test/logs/okre_0")
    # parser.add_argument("-o", help="output log file", default="res/result.log")
    # parser.add_argument("--figname", type=str, default='figname')
    # parser.add_argument("-n", action='store_true')
    # parser.add_argument("--range", type=str, default='0:200')
    # parser.add_argument("--recon", type=str, default="rec")
    # parser.add_argument("--seq", action='store_true',default=False)
    # parser.add_argument('-d', action='store_true', help='Only drawing, no test.')
    parser.add_argument("--path", help="directory of the log files", default="None")
    
    
    path = parser.parse_args().path
    if path == "None":
        name = config_dict['test_name']
        path = f"archive/{name}"
        path_list = os.listdir(path)
        # find the latest timestamp
        path_list = sorted(path_list)
        path = os.path.join(path, path_list[-1])
        
        print(path)
        # exit()
        
        
    sender_log = os.path.join(path, 'log_send_0')
    receiver_log = os.path.join(path, 'log_recv_0')
    recon_file = os.path.join(path, 'recon.yuv')
    
    
        
    reference_yuv = config_dict['video_file']
    
    cmd = f"python3 QRdec.py {recon_file} -r {reference_yuv} -o {os.path.join(path, 'quality_seq.json')} "
    
    
    os.system(cmd)
    
    cmd = f'rm -f {recon_file}'
    
    os.system(cmd)
    
    # json load {os.path.join(path, 'quality_seq.json')
    with open(os.path.join(path, 'quality_seq.json')) as f:
        quality_dict = json.load(f)
        # print(quality_dict)
    
    psnr_raw = quality_dict['psnr']
    ssim = quality_dict['ssim']
    sequence = quality_dict['seq']
    
    # print(len(sequence))
    
    # open receiver_log
    with open(receiver_log) as f:
        lines = f.readlines()
        # print(lines)
        
    # open sender_log
    with open(sender_log) as f:
        send_lines = f.readlines()
        # print(lines)
    
    lines_recv = []
    for line in lines:
        # [003:578][357706] (fake_wnd.cc:216): Frame received 3409587441 85457717
        if "Frame received" in line:
            lines_recv.append(line)
    
    print(len(lines_recv))
    print(len(sequence))
    
    # frame ID starts from 1
    size = sequence[-1] + 1
    encoding_latency = [None for i in range(size)]
    latency = [None for i in range(size)]
    psnr = [None for i in range(size)]
    sizes = [None for i in range(size)]
    fps_list = [None for i in range(size)]
    bwe_list = [None for i in range(size)]
    encoding_bitrate_list = [None for i in range(size)]
    
    for index,line in enumerate(lines_recv):
        if index >= len(sequence):
            break
        seq = sequence[index]
        
        elements = line.strip().split(' ')
        if len(elements) < 6:
            continue
        # print(elements)
        rtp_time, recv_time = elements[-2], elements[-1]
        # print("recv",rtp_time, recv_time)
        
        # find the corresponding send time based on rtp_time
        send_time = None
        coded_time = None
        for send_line in send_lines:
            if rtp_time in send_line:
                elements_send = send_line.strip().split(' ')
                # print(elements_send)
                send_time = elements_send[4]
                # print("send",rtp_time, send_time)
                break
        
        if not send_time:
            # print("send time not found!")
            exit()
        
        send_index = 0
        # again find lines with send_time
        for send_line in send_lines:
            if send_time in send_line and "LOG_SEND" in send_line:
                send_index = send_lines.index(send_line)
                ele = send_line.strip().split(' ')
                # print("",ele)
                coded_time,size = ele[-2], ele[-4]
                # print("after encoding ",cap_time)
                break
        
        if send_index != 0:
            # find the previous lines for fps, bwe, encoding bitrate;
            
            fps = None
            start_index = send_index - 1
            for i in range(start_index, 0, -1):
                if "fps = " in send_lines[i]:
                    # print(send_lines[i])
                    
                    fps = int(send_lines[i].split("fps = ")[1].split(",")[0])
                    break
            
            bwe = None
            start_index = send_index - 1
            for i in range(start_index, 0, -1):
                if "estimate_bps=" in send_lines[i]:
                    bwe = int(send_lines[i].split("estimate_bps=")[1])
                    break
            
            encoding_bitrate = None
            start_index = send_index - 1
            for i in range(start_index, 0, -1):
                if "OnBitrateUpdated" in send_lines[i]:
                    bitrate = send_lines[i].split("bitrate ")[1].split(" ")[0]
                    encoding_bitrate  = int(bitrate)
                    break
            
        if not coded_time:
            print("cap time not found!")
            exit()
        
        if not fps:
            print("fps not found!")
            exit()
        
        if not bwe:
            print("bwe not found!")
            exit()

        if not encoding_bitrate:
            print("encoding bitrate not found!")
            exit()
        
        fps_list[seq] = fps
        bwe_list[seq] = bwe
        encoding_bitrate_list[seq] = encoding_bitrate
        
        # print(seq)
        encoding_latency[seq] = int(coded_time) - int(send_time)
        latency[seq] = int(recv_time) - int(send_time)
            
        psnr[seq] = psnr_raw[index]
        sizes[seq] = size
    
    # json dump the result
    result_dict = {}
    result_dict['encoding_latency'] = encoding_latency
    result_dict['latency'] = latency
    result_dict['psnr'] = psnr
    result_dict['size'] = sizes
    result_dict['fps'] = fps_list
    result_dict['bwe'] = bwe_list
    result_dict['encoding_bitrate'] = encoding_bitrate_list
    
    
    with open(os.path.join(path, 'result.json'), 'w') as f:
        # dump with readable format
        json.dump(result_dict, f, indent=4)
        
    
    print("done")
    
cmd = f"python3 serial.py {path}"
os.system(cmd)
    

            
            
            
            
    
    