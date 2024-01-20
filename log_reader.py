
class Frame:
    def __init__(self, frame_size, timestamp,md5,intra):
        self.frame_size = frame_size
        self.sendms = timestamp
        self.recvms = None
        self.md5 = md5
        self.intra = bool(int(intra))
    def delay(self):
        if self.recvms:
            return self.recvms - self.sendms
        else:
            return None
    def __str__(self):
        if self.intra:
            frame = "I"
        else:
            frame = "P"
        
        st = f"{frame} Frame: size={self.frame_size},  delay={self.delay()}, sendms={self.sendms}, recvms={self.recvms}, md5={self.md5},"
        return st


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        res_log_name = "res.log"
    else:
        res_log_name = sys.argv[1]
        
    # log_dir = "/home/jiee/sparkrtc/out/t/logs/"
    
    # import os
    # file_list = os.listdir(log_dir)
    # sender_logs = [i for i in file_list if 's.l' in i]
    # receiver_logs = [i for i in file_list if 'r.l' in i]
    
    # se
    # # sort by timestamp
    # sender_logs.sort()
    # receiver_logs.sort()
    # print(sender_logs)
    # print(receiver_logs)
    sender_log = "logs/sender.log"
    receiver_log = "logs/receiver.log"
    
    print(sender_log)
    print(receiver_log)
    
    

    lines_sender = []
    with open(sender_log) as f:
        lines_sender = f.readlines()

    lines_receiver = []
    with open(receiver_log) as f:
        lines_receiver = f.readlines()


    sended_frames = []
    for line in lines_sender:
        if 'LOGSEN' in line:
            line = line.strip()
            # print(line)
            _,_,_,size,timestamp,md5,intra = line.split()
            frame = Frame(int(size), int(timestamp),md5,intra)
            sended_frames.append(frame)

    recv_dict = {}
    duplicate_symbol = []
    for line in lines_receiver:
        if 'LOGREC' in line:
            line = line.strip()
            # print(line)
            _,_,_,size,timestamp,md5,intra = line.split()
            if md5 in recv_dict:
                print("Duplicate md5, ignored " + size,md5)
                duplicate_symbol.append(md5)
            else:
                recv_dict[md5] = int(timestamp)

    total_delay = []
    resf = open(res_log_name, 'w')
    for frame in sended_frames:
        if frame.md5 not in duplicate_symbol:
            if frame.md5 in recv_dict:
                frame.recvms = recv_dict[frame.md5]
            else:
                print("Frame not received: " + str(frame))
                resf.write("Frame not received: " + str(frame) + "\n")
                
        if frame.delay() != None:
            total_delay.append(frame.delay())
            print(frame)
            resf.write(str(frame) + "\n")
            
    print("Average delay: " + str(sum(total_delay) / len(total_delay)))
    resf.write("Average delay: " + str(sum(total_delay) / len(total_delay)))
    resf.close()