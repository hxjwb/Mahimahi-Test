import cv2
from pyzbar import pyzbar
import numpy as np
from skimage.metrics import structural_similarity as ssim


QRcodeSize = 290
def decode_qr_code(image):
    
    # valid block size is QRcodeSize
    code_block = image[0:QRcodeSize, 0:QRcodeSize]
    
    # Decode QR code using pyzbar
    decoded_objects = pyzbar.decode(code_block)
    
    # Extract information from decoded objects
    qr_code_info = ""
    for obj in decoded_objects:
        data = obj.data.decode("utf-8")
        qr_code_info += data
    
    if not qr_code_info:
        print(f"Frame {f}: No QR code detected")
        

    # print(f"Frame {f}: {qr_code_info}")
    try:
        _, frame_number = qr_code_info.split(' ')
        
        frame_number = int(frame_number)
        
        return frame_number
    except:
        print(f"Frame {f}: Invalid QR code")
        return -1



if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='Decode YUV file with QR code into text')
    parser.add_argument('file', help='input yuv file')
    parser.add_argument('-s', type=str, default='1920x1080', help='Input YUV size, default is 1920x1080')
    parser.add_argument('-r', type=str, default='yuv_coded.yuv', help='referenced yuv file')
    parser.add_argument('-o', type=str, default='metric.json', help='Output json file for metrics')
    # parser.add_argument('-v', type=str, default='out.yuv', help='YUV for vmaf')
    args = parser.parse_args()
    
    
    # ref_yuv_file = args.v
    # Specify the file path, width, and height
    file_path = args.file
    file_ref = args.r
    w, h = map(int, args.s.split('x'))

    # read yuv file
    yuvfile = open(file_path, 'rb')
    yuvfile_ref = open(file_ref, 'rb')
    # yuvfile_vmaf = open(ref_yuv_file, 'wb')
    output_name = args.o
    
    # get frame count
    yuvfile.seek(0, 2)
    yuv_size = yuvfile.tell()
    yuvfile.seek(0, 0)
    frame_count = yuv_size // (h*w*3//2)
    print('frame_count', frame_count)
    
        
    output = {}
    output['psnr'] = []
    output['ssim'] = []
    output['seq']  = []
    for f in range(frame_count):
        
        # read 1 frame
        yuv_buf = yuvfile.read(h*w*3//2)
        
        yuv_data = np.frombuffer(yuv_buf, dtype=np.uint8).reshape((h + h // 2, w))
        bgr = cv2.cvtColor(yuv_data, cv2.COLOR_YUV2BGR_I420)
        
        frame_number = decode_qr_code(bgr)

        output['seq'].append(frame_number)
        # print(bgr.shape)
        
        if frame_number != -1:
        # seek to the same frame in the reference file
            yuvfile_ref.seek(frame_number * h * w * 3//2, 0)
            
            # read 1 frame
            yuv_buf = yuvfile_ref.read(h*w*3//2)
            
            # yuvfile_vmaf.write(yuv_buf)
            
            yuv_data = np.frombuffer(yuv_buf, dtype=np.uint8).reshape((h + h // 2, w))
            
            ref_bgr = cv2.cvtColor(yuv_data, cv2.COLOR_YUV2BGR_I420)
            
            frame_number_ref = decode_qr_code(ref_bgr)
            
            if frame_number != frame_number_ref:
                print(f"Frame {f}: Frame number mismatch: {frame_number} vs {frame_number_ref}")
                exit(0)
            
            # print(ref_bgr.shape)
            # get psnr and ssim
            psnr = cv2.PSNR(bgr, ref_bgr)
            
            
            # ssim_ = ssim(bgr, ref_bgr, multichannel=True, channel_axis = 2)
            
            # print(f"Frame {f}: PSNR: {psnr:.2f}", f"SSIM: {ssim_:.2f}")
        
            output['psnr'].append(psnr)
            # output['ssim'].append(ssim_)
        
        else:
            output['psnr'].append(0)
            # output['ssim'].append(0)
        

    yuvfile.close()
    yuvfile_ref.close()
    # yuvfile_vmaf.close()
    import json
    with open(output_name, 'w') as f:
        json.dump(output, f)
    