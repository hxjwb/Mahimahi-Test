
import os

queue_size = 100
only_draw = False
st,ed = 0, 100
show_numbers = False

def change_action(action):
    cc_path = "/home/xiangjie/sparkrtc/modules/pacing/pacing_controller.cc"
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

def change_complexity(c):
    cc_path = "/home/xiangjie/sparkrtc/modules/video_coding/codecs/h264/h264_encoder_impl.cc"
    file = open(cc_path, "r")
    lines = file.readlines()
    file.close()
    
    index = -1
    for line in lines:
        if '#define PRESET' in line and '//' not in line:
            print(lines.index(line))
            index = lines.index(line)
    
    # if not found
    if index == -1:
        exit(1)
    lines[index] = f'#define PRESET {c}\n'


    # write to cc file
    file = open(cc_path, "w")
    file.writelines(lines)
    file.close()
    

def change_vbv(c):
    cc_path = "/home/xiangjie/sparkrtc/modules/video_coding/codecs/h264/h264_encoder_impl.cc"
    file = open(cc_path, "r")
    lines = file.readlines()
    file.close()
    
    index = -1
    for line in lines:
        if '#define VBV' in line and '//' not in line:
            print(lines.index(line))
            index = lines.index(line)
    
    # if not found
    if index == -1:
        exit(1)
    lines[index] = f'#define VBV {c}\n'


    # write to cc file
    file = open(cc_path, "w")
    file.writelines(lines)
    file.close()


def change_cbr(c):
    cc_path = "/home/xiangjie/sparkrtc/modules/video_coding/codecs/h264/h264_encoder_impl.cc"
    file = open(cc_path, "r")
    lines = file.readlines()
    file.close()
    
    index = -1
    for line in lines:
        if '#define CBR' in line and '//' not in line:
            print(lines.index(line))
            index = lines.index(line)
    
    # if not found
    if index == -1:
        exit(1)
    lines[index] = f'#define CBR {c}\n'


    # write to cc file
    file = open(cc_path, "w")
    file.writelines(lines)
    file.close()


def change_factor(c):
    cc_path = "/home/xiangjie/sparkrtc/video/video_stream_encoder.cc"
    file = open(cc_path, "r")
    lines = file.readlines()
    file.close()
    
    index = -1
    for line in lines:
        if '#define FACTOR' in line and '//' not in line:
            print(lines.index(line))
            index = lines.index(line)
    
    # if not found
    if index == -1:
        exit(1)
    lines[index] = f'#define FACTOR {c}\n'


    # write to cc file
    file = open(cc_path, "w")
    file.writelines(lines)
    file.close()
    

    
def change_pace(pace):
    cc_path = "/home/xiangjie/sparkrtc/modules/congestion_controller/goog_cc/goog_cc_network_control.cc"

    file = open(cc_path, "r")
    lines = file.readlines()
    file.close()


    # index = -1
    # for line in lines:
    #     if 'pacing_factor_ = ' in line and '//' not in line:
    #         print(lines.index(line))
    #         index = lines.index(line)
    # if pace:
    #     lines[index] = '  pacing_factor_ = 1.0f;\n'
    # else:
    #     lines[index] = '  pacing_factor_ = 100.0f;\n'

    
    index = -1
    for line in lines:
        if 'pacing_factor_ =' in line and '//' not in line:
            print(lines.index(line))
            index = lines.index(line)
    
    # if not found
    if index == -1:
        exit(1)
    lines[index] = f'  pacing_factor_ = {pace}.0f;\n'
    
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

    # -d
    only_draw_str = ""
    if only_draw:
        only_draw_str = "-d"
    cmd = f"python3 log_reader.py {shownumber_str} -s logs/{logsend}_0 -r logs/{logrecv}_0 --figname res/{figname} --range {st}:{ed} -o res/{name}.log --recon res/{name}.yuv --seq {only_draw_str}"
    os.system(cmd)


def compile():
    os.system("cd /home/xiangjie/sparkrtc && ninja -C out/t")
    
def run2(name):
    import json 
    # load config.json
    with open('config.json') as f:
        config = json.load(f)
    config['test_name'] = name
    
    # write to config.json
    with open('config.json', 'w') as f:
        json.dump(config, f)
    
    os.system("python3 run.py")
    
    # os.system(f"sudo cp -r archive/{name} /var/www/html/t2/")
    
    

if __name__ == "__main__":
    # import argparse
    # parser = argparse.ArgumentParser()
    # parser.add_argument('-d', action='store_true', help='Only drawing, no test.')
    # parser.add_argument('-q', type=int, default=500, help='Queue size.')
    # parser.add_argument('-c', action='store_true', help='Compare.',default=False)
    # parser.add_argument('-r',type=str, help='Range.',default="0:500")
    # parser.add_argument('-n', action='store_true', help='Show size numbers',default=False)
    
    # queue_size = parser.parse_args().q
    # only_draw = parser.parse_args().d
    # st,ed = parser.parse_args().r.split(':')
    # st = int(st)
    # ed = int(ed)
    # compare = parser.parse_args().c
    # show_numbers = parser.parse_args().n
    
    # if compare:
    #     change_pace(True)
    #     change_action(False)
    #     run("pace")
    
    # change_pace(False) # 100.0
    # change_action(False) # token bucket
    
    
    # run("CBR0")
    
    
    # CBR test
    # change_pace(False)  
    
    # for i in range(4, 10, 2):
    #     change_vbv(i)
    #     compile()
    #     run2(f"test_fix_bitrate{i}")
    
    # our test
    # change_pace(False) # 100.0
    # change_factor("1.0")
    # compile()
    # run2("ours")
    
    # Ours vbv test
    # change_pace(False) # 100.0
    
    # for i in range(4, 5, 2):
    #     vbv = i / 2
    #     vbv = str(vbv)
    #     change_vbv(vbv)
    #     compile()
    #     run2(f"auto_vbv_{i}")
    
    
    # CBR qp - delay test
    # change_pace(False)
    
    # for i in range(11, 16, 1):
        
    #     factor = i / 10
    #     factor_str = str(factor)
        
    #     change_factor(factor_str)
    #     compile()
    #     run2(f"auto_CBR_factor_{factor_str}")
    
    
    # CBR real 
    # change_pace(False)
    # change_vbv(1)
    
    # change_vbv(1)
    # change_cbr(1)
    # compile()
    # run2("CBR0429")
    
    # change_cbr(0)
    # change_vbv(3)
    # compile()
    # run2("VBV_3")
    
    
    # change_cbr(0)
    # change_pace(100)
    # change_vbv(3)
    # compile()
    # run2("Pacing")
    
    change_cbr(0)
    change_vbv(20)
    change_pace(100)
    change_factor("1.0")
    compile()
    run2("networking")
    
    
    # change_cbr(0)
    # change_vbv(10)
    # compile()
    # run2("VBV_10")
    
    # for i in range(7, 15, 2):
    #     change_cbr(1)
    #     change_vbv(1)
    #     change_factor(str(i/10))
    #     compile()
    #     run2(f"CBR_factor_{str(i/10)}")
        
    # change_vbv(1)
    # change_cbr(1)
    # compile()
    # run2("CBR0429")
    
    
    