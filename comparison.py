
import os



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

def run(name,only_draw=False):
    qs = 300
    st,ed = 0, 100
    # name = "pace_no"
    logsend = f'{name}_send' 
    logrecv = f'{name}_recv'
    figname = f'{name}'
    
    if not only_draw:
        # compile
        os.system("cd /home/xiangjie/sparkrtc && ninja -C out/t")

        # Test
        os.system(f"cd /home/xiangjie/Mahimahi-Test/ && python3 webrtc_test.py --recon res/{name}.yuv --queue {qs} --logsend {logsend} --logrecv {logrecv}  --figname {figname}")

    # Draw
    cmd = f"python3 log_reader.py -s logs/{logsend}_0 -r logs/{logrecv}_0 --figname res/{figname} --range {st}:{ed} -o res/{name}.log"
    os.system(cmd)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', action='store_true', help='Only drawing, no test.')
    
    change_pace(True)
    run("pace",parser.parse_args().d)
    
    change_pace(False)
    run("ours",parser.parse_args().d)