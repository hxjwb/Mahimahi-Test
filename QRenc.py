# Description: read yuv file and show rgb image with opencv
# Author: HUANG XIANGJIE

import cv2
import numpy as np
from tqdm import tqdm


def parse_args():
    import argparse
    parser = argparse.ArgumentParser()

    parser.add_argument('file', type=str, help='yuv file',default='/home/xiangjie/new.yuv')
    
    parser.add_argument('-s', type=str, default='1920x1080', help='Input YUV size, default is 1920x1080')
    parser.add_argument('-o', type=str, default='yuv_coded.yuv', help='Output YUV file')
    
    args = parser.parse_args()
    return args


def generate_qrcode( data = 'frame 1'):
    import qrcode
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=3,
    )
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image()

    qs = img.size[1]
    img = np.array(img.getdata()).reshape(img.size[1], img.size[0])
    
    
    return img,qs



if __name__ == '__main__':
    # parse arguments

    args = parse_args()
    
    # set values
    yuvfile = args.file
    outputfile = args.o
    
    try:
        w, h = args.s.split('x')
        w = int(w)
        h = int(h)
        # w, h = 1920, 1080
    except:
        print('Input YUV size is invalid. Please input like 1920x1080')
        exit(0)

    
    # read yuv file
    yuvfile = open(yuvfile, 'rb')
    
    # get frame count
    yuvfile.seek(0, 2)
    yuv_size = yuvfile.tell()
    yuvfile.seek(0, 0)
    frame_count = yuv_size // (h*w*3//2)
    print('frame_count', frame_count)
    
    
    # save yuv_data to yuv file
    yuvfile_code = open(outputfile, 'wb')
        
    for f in tqdm(range(frame_count)):
        
        # read 1 frame
        yuv_buf = yuvfile.read(h*w*3//2)
        
        # split yuv data
        y_buf = yuv_buf[0:h*w]
        u_buf = yuv_buf[h*w:h*w+h*w//4]
        v_buf = yuv_buf[h*w+h*w//4:h*w+h*w//4+h*w//4]
        
        # convert to numpy array
        y_data = np.frombuffer(y_buf, dtype=np.uint8).reshape(h, w)
        u_data = np.frombuffer(u_buf, dtype=np.uint8).reshape(h//2, w//2)
        v_data = np.frombuffer(v_buf, dtype=np.uint8).reshape(h//2, w//2)
        
        # generate qrcode
        qrcode_block,qs = generate_qrcode(f'f {f}')
        
        # copy qrcode to y data
        y_data_code = y_data.copy()
        y_data_code[0:qs, 0:qs] = qrcode_block
        
        # set u and v data 127
        u_data_code = u_data.copy()
        u_data_code[0:qs//2, 0:qs//2] = 127

        v_data_code = v_data.copy()
        v_data_code[0:qs//2, 0:qs//2] = 127
        
        # save to output file
        code_buf_y = y_data_code.tobytes()
        code_buf_u = u_data_code.tobytes()
        code_buf_v = v_data_code.tobytes()
        
        yuvfile_code.write(code_buf_y)
        yuvfile_code.write(code_buf_u)
        yuvfile_code.write(code_buf_v)
        
        
             
    yuvfile_code.close()
    yuvfile.close()
    
    
    
    
    