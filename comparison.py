
import os

queue_size = 100
only_draw = False
st,ed = 0, 100
show_numbers = False

def change_action(action):
    cc_path = "/home/xiangjie/sparkrtc/modules/video_coding/codecs/av1/libaom_av1_encoder.cc"
    file = open(cc_path, "r")
    lines = file.readlines()
    file.close()
    
    index = -1
    for line in lines:
        if '#define ACTION' in line and '//' not in line:
            print(lines.index(line))
            index = lines.index(line)
    if action:
        lines[index] = '#define ACTION 1\n'
    else:
        lines[index] = '#define ACTION 0\n'

    # write to cc file
    file = open(cc_path, "w")
    file.writelines(lines)
    file.close()


    

    
def change_pace(pace):
    cc_path = "/home/xiangjie/sparkrtc/modules/congestion_controller/goog_cc/goog_cc_network_control.cc"

    file = open(cc_path, "r")
    lines = file.readlines()
    file.close()


    index = -1
    for line in lines:
        if 'pacing_factor_ = ' in line and '//' not in line:
            print(lines.index(line))
            index = lines.index(line)
    if pace:
        lines[index] = '  pacing_factor_ = 1.0f;\n'
    else:
        lines[index] = '  pacing_factor_ = 100.0f;\n'

    # write to cc file
    file = open(cc_path, "w")
    file.writelines(lines)
    file.close()
    

def run(name):

    # st,ed = 0, 100
    # name = "pace_no"
    logsend = f'{name}_send' 
    logrecv = f'{name}_recv'
    figname = f'{name}'
    
    if not only_draw:
        # compile
        os.system("cd /home/xiangjie/sparkrtc && ninja -C out/t")

        # Test
        os.system(f"cd /home/xiangjie/Mahimahi-Test/ && python3 webrtc_test.py --recon res/{name}.yuv --queue {queue_size} --logsend {logsend} --logrecv {logrecv}  --figname {figname}")

    # Draw
    shownumber_str = ""
    if show_numbers:
        shownumber_str = "-n"
    cmd = f"python3 log_reader.py {shownumber_str} -s logs/{logsend}_0 -r logs/{logrecv}_0 --figname res/{figname} --range {st}:{ed} -o res/{name}.log"
    os.system(cmd)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', action='store_true', help='Only drawing, no test.')
    parser.add_argument('-q', type=int, default=130, help='Queue size.')
    parser.add_argument('-c', action='store_true', help='Compare.',default=False)
    parser.add_argument('-r',type=str, help='Range.',default="0:500")
    parser.add_argument('-n', action='store_true', help='Show size numbers',default=False)
    
    queue_size = parser.parse_args().q
    only_draw = parser.parse_args().d
    st,ed = parser.parse_args().r.split(':')
    st = int(st)
    ed = int(ed)
    compare = parser.parse_args().c
    show_numbers = parser.parse_args().n
    
    if compare:
        change_pace(True)
        change_action(False)
        run("pace")
    
    change_pace(False)
    change_action(True)
    run("ours")