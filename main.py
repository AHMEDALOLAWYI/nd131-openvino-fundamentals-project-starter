"""People Counter."""
"""
 Copyright (c) 2018 Intel Corporation.
 Permission is hereby granted, free of charge, to any person obtaining
 a copy of this software and associated documentation files (the
 "Software"), to deal in the Software without restriction, including
 without limitation the rights to use, copy, modify, merge, publish,
 distribute, sublicense, and/or sell copies of the Software, and to
 permit person to whom the Software is furnished to do so, subject to
 the following conditions:
 The above copyright notice and this permission notice shall be
 included in all copies or substantial portions of the Software.
 THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
 EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
 MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
 NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
 LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
 OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
 WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""


import os
import sys
import time
import socket
import json
import cv2
import math

import logging as log
import paho.mqtt.client as mqtt

from argparse import ArgumentParser
from inference import Network

# MQTT server environment variables
HOSTNAME = socket.gethostname()
IPADDRESS = socket.gethostbyname(HOSTNAME)
MQTT_HOST = IPADDRESS
MQTT_PORT = 3001
MQTT_KEEPALIVE_INTERVAL = 60

def build_argparser():
    """
    Parse command line arguments.

    :return: command line arguments
    """
    parser = ArgumentParser()
    parser.add_argument("-m", "--model", required=True, type=str,
                        help="Path to an xml file with a trained model.")
    parser.add_argument("-i", "--input", required=True, type=str,
                        help="Path to image or video file")
    parser.add_argument("-l", "--cpu_extension", required=False, type=str,
                        default=None,
                        help="MKLDNN (CPU)-targeted custom layers."
                             "Absolute path to a shared library with the"
                             "kernels impl.")
    parser.add_argument("-d", "--device", type=str, default="CPU",
                        help="Specify the target device to infer on: "
                             "CPU, GPU, FPGA or MYRIAD is acceptable. Sample "
                             "will look for a suitable plugin for device "
                             "specified (CPU by default)")
    parser.add_argument("-pt", "--prob_threshold", type=float, default=0.55,
                        help="Probability threshold for detections filtering"
                        "(0.55 by default)")
    return parser


def connect_mqtt():
    # Connect to the MQTT server
    client = mqtt.Client()
    client.connect(MQTT_HOST, MQTT_PORT, MQTT_KEEPALIVE_INTERVAL)
    return client

def draw_outputs(coords, frame, initial_w, initial_h, x, k, prob_threshold):
        current_count = 0     
        ed_distance = x
        for detections in coords[0][0]:
            #  Drawing Bounding box 
            if detections[2] > prob_threshold:
                xmin = int(detections[3] * initial_w)
                ymin = int(detections[4] * initial_h)
                xmax = int(detections[5] * initial_w)
                ymax = int(detections[6] * initial_h)
                cv2.rectangle(frame, (xmin, ymin), (xmax, ymax), (0,255, 0), 4)
                current_count = current_count + 1
                #print(initial_count)
                
                c_x = frame.shape[1]/2
                c_y = frame.shape[0]/2    
                mid_x = (xmax + xmin)/2
                mid_y = (ymax + ymin)/2
                
                # Calculating distance 
                ed_distance =  math.sqrt(math.pow(mid_x - c_x, 2) +  math.pow(mid_y - c_y, 2) * 1.0) 
                k = 0

        if current_count < 1:
            k += 1
            
        if ed_distance>0 and k < 10:
            current_count = 1 
            k += 1 
            if k > 100:
                k = 0
                
        return frame, current_count, ed_distance, k

def infer_on_stream(args, client):
    # Initialise the class
    infer_network = Network()
    # Set Probability threshold for detections
    model=args.model
    video_file=args.input    
    extn=args.cpu_extension
    device=args.device
    #prob_threshold = args.prob_threshold
    
    # Flag for the input image
    single_img_flag = False

    start_time = 0
    cur_request_id = 0
    last_count = 0
    total_count = 0
    
    # Load the model through `infer_network`  and handle the input stream
    n, c, h, w = infer_network.load_model(model, device, 1, 1, cur_request_id, extn)[1]

    # check for live video 
    if video_file == 'CAM': 
        input_stream = 0

    elif video_file.endswith('.jpg') or video_file.endswith('.bmp') :    
        single_img_flag = True
        input_stream = video_file

    else:     # Check for video file
        input_stream = video_file
        if not os.path.isfile(video_file):
            print("file doesn't exist")



			
    
    try:
        cap=cv2.VideoCapture(video_file)
    except FileNotFoundError:
        print("Cannot locate video file: "+ video_file)
    
    
    total_count = 0  
    duration = 0
    
    initial_w = cap.get(3)
    initial_h = cap.get(4)
    prob_threshold = args.prob_threshold
    temp = 0
    tk = 0
    current_frame = 0
    fps = cap.get(cv2.CAP_PROP_FPS)
    
    # Loop until stream is over
    while cap.isOpened():
        # Read from the video capture
        flag, frame = cap.read()
        if not flag:
            break
        key_pressed = cv2.waitKey(60)
        # Image Pre-processing and initating async inference
        image = cv2.resize(frame, (w, h))
        # Tanspose and reshape the image 
        image = image.transpose((2, 0, 1))
        image = image.reshape((n, c, h, w))
        
        # Start asynchronous inference for specified request
       
        infer_network.exec_net(cur_request_id, image)
        
        color = (255,0,0)

        # Wait for the result
        if infer_network.wait(cur_request_id) == 0:
            

            # Get the results of the inference request 
            result = infer_network.get_output(cur_request_id)
            
            # Draw Bounting Box
            frame, current_count, d, tk = draw_outputs(result, frame, initial_w, initial_h, temp, tk, prob_threshold)
            
        
            # Calculate and send relevant information 
            if current_count > last_count: # New entry
                
                start_frame = current_frame
                total_count = total_count + current_count - last_count
                client.publish("person", json.dumps({"total": total_count}))            
            
            if current_count < last_count: # Average Time
                
                end_frame = current_frame - start_frame 
                client.publish("person/duration", json.dumps({"duration": end_frame/fps}))
                
           
            
            client.publish("person", json.dumps({"count": current_count})) # People Count

            last_count = current_count
            temp = d

            if key_pressed == 27:
                break

        # Send the frame to the FFMPEG server
        sys.stdout.buffer.write(frame) 
        current_frame = current_frame + 1 
        sys.stdout.flush()
        
        #Save the Image
        if single_img_flag:
            cv2.imwrite('output_image.jpg', frame)
       
    cap.release()
    cv2.destroyAllWindows()
    client.disconnect()
    infer_network.clean()

def main():
    # Grab command line args
    args = build_argparser().parse_args()
    # Connect to the MQTT server
    client = connect_mqtt()
    # Perform inference on the input stream
    infer_on_stream(args, client)


if __name__ == '__main__':
    main()
