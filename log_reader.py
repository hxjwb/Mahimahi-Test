
class Frame:
    def __init__(self, frame_size, captured_time,encoded_time,md5):
        self.frame_size = frame_size
        self.sendms = encoded_time
        self.capms = captured_time
        self.recvms = None
        self.decms = None
        self.md5 = md5
        self.bps = None
        self.nack = None
        self.fps = None
        self.pid = None
        self.bitrate = None # encoding bitrate
        # self.intra = bool(int(intra))
    def net_delay(self):
        if self.recvms:
            return self.recvms - self.sendms
        else:
            return None
    def decode_delay(self):
        if self.decms:
            return self.decms - self.recvms
        else:
            return None
    def encode_delay(self): 
        return self.sendms - self.capms
    def total_delay(self):
        if self.decms:
            return self.decms - self.capms
        else:
            return None
    def __str__(self):
        # if self.intra:
        #     frame = "I"
        # else:
        #     frame = "P"
        frame = 'Unknown'
        st = f"{frame} Frame: size={self.frame_size}, net_delay={self.net_delay()}, decode_delay={self.decode_delay()}, encode_delay={self.encode_delay()}, total_delay={self.total_delay()}, md5={self.md5}"
        return st


def read_loss_from_mahimahi_log(logfile):
    # logfile = 'logs/mah.log'

    lines = []

    with open(logfile) as f:
        lines = f.readlines()

    packet_per_ms = {}

    ts = 0
    for line in lines:
        if " d " in line:
            line = line.strip()
            # print(line)
            ts, _, num, size, pack_ts = line.split(' ')
            pack_ts = int(pack_ts)
            if pack_ts not in packet_per_ms:
                packet_per_ms[pack_ts] = 0
            packet_per_ms[pack_ts] += 1
    
    return packet_per_ms


if __name__ == "__main__":
    
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", help="sender log file", default="/home/xiangjie/Mahimahi-Test/logs/np_pace_0")
    parser.add_argument("-r", help="receiver log file", default="/home/xiangjie/Mahimahi-Test/logs/okre_0")
    parser.add_argument("-o", help="output log file", default="res/result.log")
    parser.add_argument("--figname", type=str, default='figname')
    parser.add_argument("-n", action='store_true')
    parser.add_argument("--range", type=str, default='0:200')
    
    
    res_log_name = parser.parse_args().o
    sender_log = parser.parse_args().s
    receiver_log = parser.parse_args().r
    figname = parser.parse_args().figname
    show_num = parser.parse_args().n
    st,ed = parser.parse_args().range.split(':')
    st = int(st)
    ed = int(ed)
    # print(sender_log)
    # print(receiver_log)
    
    

    lines_sender = []
    with open(sender_log) as f:
        lines_sender = f.readlines()

    lines_receiver = []
    with open(receiver_log) as f:
        lines_receiver = f.readlines()


    sended_frames = []
    last_line = 0
    valued_lines_index = []
    for i,line in enumerate(lines_sender):
        if 'LOG_SEND' in line:
            
            valued_lines_index.append(i)
            line = line.strip()
            
            # get the frame size, captured time, encoded time, md5
            # print(line): LOG_SEND|size|captured_time|encoded_time|md5 9102 2221929827 2221929943 c2f4168f8b5dd6e48c1536b9a3f43a02
            _,_,_,size,captured_time,encoded_time,md5 = line.split(" ")
            frame = Frame(int(size), int(captured_time),int(encoded_time),md5)
            
            # Get the bps before encoding this frame
            index = i
            while True:
                index -= 1
                if 'estimate_bps=' in lines_sender[index]:
                    valued_lines_index.append(index)
                    frame.bps = int(lines_sender[index].split("estimate_bps=")[1])
                    break
            
            # Get the fps before this frame
            index = i
            while True:
                index -= 1
                if 'fps = ' in lines_sender[index]:
                    valued_lines_index.append(index)
                    frame.fps = int(lines_sender[index].split("fps = ")[1].split(",")[0])
                    break
            
            index = i
            while True:
                index -= 1
                # [006:671][313155] (video_stream_encoder.cc:2348): OnBitrateUpdated, bitrate 5519592 stable bitrate = 2136347 link allocation bitrate = 5519592 packet loss 0 rtt 43
                if 'OnBitrateUpdated' in lines_sender[index]:
                    valued_lines_index.append(index)
                    # print(lines_sender[index])
                    bitrate = lines_sender[index].split("bitrate ")[1].split(" ")[0]
                    frame.bitrate = int(bitrate)
                    # print(bitrate)
                    break

            
            # Get the packet id(RTP timestamp)
            try:
                next_lines = lines_sender[i+1 : i + 30]
                for ind,nline in enumerate(next_lines):
                    if "Packet ID:" in nline:
                        valued_lines_index.append(ind)
                        nline = nline.strip()
                        pid = nline.split("Packet ID:")[1]
                        pid = int(pid)
                        frame.pid = pid
                        # print(pid)
                        break
                if not frame.pid:
                    print("no id found")
                    print(line)
            except:
                continue
            
            # get the nacks between this frame and the last frame
            nacks = 0
            for i in range(last_line, index):
                if "LOGNACK for" in lines_sender[i]:
                    valued_lines_index.append(i)
                    stt = lines_sender[i].strip()
                    nack = stt.split("LOGNACK for")[1].split(' ')[1]
                    nack = int(nack)
                    nacks += nack
                    
            frame.nack = nacks * 1300
            sended_frames.append(frame)
            last_line = index

    lines_valued = []
    for i,line in enumerate(lines_sender):
        if i in valued_lines_index:
            lines_valued.append(line)
    with open(f'{figname}_clean.log', 'w') as f:
        f.writelines(lines_valued)
    recv_dict = {}
    duplicate_symbol = []
    for line in lines_receiver:
        if 'LOG_RECV' in line:
            line = line.strip()
            # print(line)
            # print(line) LOG_RECV|size|decode_time|decoded_time|md5 9102 2221930011 2221930041 c2f4168f8b5dd6e48c1536b9a3f43a02
            try:
                _,_,_,size,recv_time,decoded_time,md5 = line.split(" ")
                if md5 in recv_dict:
                    # print("Strange ! Duplicate md5, ignored " + size,md5)
                    duplicate_symbol.append(md5)
                else:
                    recv_dict[md5] = [int(recv_time), int(decoded_time)]
            except:
                # print("Error in line: " + line)
                continue

    total_delay = []
    resf = open(res_log_name, 'w')
    total_size = []
    
    
    
    
    for frame in sended_frames:
        if frame.md5 not in duplicate_symbol:
            if frame.md5 in recv_dict:
                frame.recvms = recv_dict[frame.md5][0]
                frame.decms = recv_dict[frame.md5][1]
            else:
                # print("Frame not received: " + str(frame))
                resf.write("Frame not received: " + str(frame) + "\n")
                
        if frame.net_delay() != None:
            total_delay.append(frame.net_delay())
            total_size.append(frame.frame_size)
            # print(frame)
            resf.write(str(frame) + "\n")
            
    # print("Average delay: " + str(sum(total_delay) / len(total_delay)))
    resf.write("Average delay: " + str(sum(total_delay) / len(total_delay)))
    resf.write("Average size: " + str(sum(total_size) / len(total_size)))
    resf.close()
    
        
   
    sizes = [frame.frame_size for frame in sended_frames]
    delays = [frame.net_delay() for frame in sended_frames]
    for i in range(len(delays)):
        if not delays[i]:
            delays[i] = 1999
    
    bytes_per_frame = [frame.bps / 8 / frame.fps for frame in sended_frames]
    enc_bytes_per_frame = [frame.bitrate / 8 / frame.fps for frame in sended_frames]
    nacks = [frame.nack for frame in sended_frames]
    
    
    import matplotlib as mpl
    mpl.use('Agg')
    import matplotlib.pyplot as plt


    
 
    # 画布大小为 10 * 6
    plt.figure(figsize=(10,6))

    plt.xlim([st,ed])
    
    bar_x = [i for i in range(len(sended_frames))]
    
    plt.bar(bar_x, sizes, label='frame size', color='Coral', alpha=0.9) 
    
    # show the frame size of each frame
    if show_num:
        for i in range(st, ed):
            plt.text(bar_x[i], sizes[i], sizes[i], ha='center', va='bottom', fontsize=7)


    # x: frame number y: frame size
    plt.xlabel('Frame Number')
    plt.ylabel('Size(Bytes)')
    
    plt.plot(bar_x, bytes_per_frame, label='BWE(bytes per frame)', c='blue', ms=5, linewidth='1.5')
    plt.plot(bar_x, enc_bytes_per_frame, label='BWE(bytes per frame)', c='green', ms=5, linewidth='1.5')

    # Average frame size
    # avg_size = sum(sizes) / len(sizes)
    # plt.axhline(y=avg_size, color='r', linestyle='--', alpha=0.5)
    
    
    
    packet_per_ms = read_loss_from_mahimahi_log('logs/mah.log')
    losses = []
    for i in range(len(bar_x) - 1):
        frame = sended_frames[i]
        pid = frame.pid
        try:
            loss = packet_per_ms[pid]
        except:
            loss = 0
        losses.append(loss * 1300)
    losses.append(0)
    plt.ylim([0, 200000])
    plt.yticks(range(0, 200000, 20000))
    plt.bar(bar_x, losses, label='losses', color='black', alpha=0.5)
    # plt.plot(bar_x, nacks, label='Nack', c='yellow', ms=5, linewidth='1.5')
    plt.legend(loc = 'upper left')
    
    plt.twinx() 
    plt.ylabel('Delays(ms)')
    plt.ylim([0, 1000])
    plt.yticks(range(0, 1000, 100))
    plt.grid()
    plt.plot(bar_x, delays, label='Delay', c='black', ms=5, linewidth='1.5')
    # 画一个 6e6 的虚线
    # plt.axhline(y=6000000, color='b', linestyle='--', alpha=0.3)
    
    plt.legend(loc = 'upper right')
    
    name = f'{figname}.png'
    plt.savefig(name)

