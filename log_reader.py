
class Frame:
    def __init__(self, frame_size, timestamp):
        self.frame_size = frame_size
        self.recvms = timestamp
        self.sendms = None
    def delay(self):
        if self.sendms:
            return self.recvms - self.sendms
        else:
            return None

sender_log = "sender.log"
receiver_log = "receiver.log"

lines_sender = []
with open(sender_log) as f:
    lines_sender = f.readlines()

lines_receiver = []
with open(receiver_log) as f:
    lines_receiver = f.readlines()


received_frames = []
for line in lines_receiver:
    if 'LOGREC' in line:
        line = line.strip()
        # print(line)
        _,_,size,timestamp = line.split()
        frame = Frame(int(size), int(timestamp))
        received_frames.append(frame)

sending_dict = {}
duplicate_frame_size = []
for line in lines_sender:
    if 'LOGSEN' in line:
        line = line.strip()
        # print(line)
        _,_,size,timestamp = line.split()
        if int(size) in sending_dict:
            print("Duplicate frame size, ignored" + size)
            duplicate_frame_size.append(int(size))
        else:
            sending_dict[int(size)] = int(timestamp)

for frame in received_frames:
    if frame.frame_size not in duplicate_frame_size:
        if frame.frame_size in sending_dict:
            frame.sendms = sending_dict[frame.frame_size]
        else:
            print("Frame size not found in sending logs which is strange" + str(frame.frame_size))

    print(frame.frame_size, frame.sendms, frame.recvms, frame.delay())
        