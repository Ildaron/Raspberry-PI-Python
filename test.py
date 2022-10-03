import cv2
from pyspin import PySpin
import numpy as np
import math
from zaber_motion import Library
from zaber_motion.binary import Connection
from zaber_motion import RequestTimeoutException
Library.enable_device_db_store()
import time
import pandas as pd

def image_processing(img, number):
    resize=25
    x = int(img.shape[1] * resize / 100)
    y = int(img.shape[0] * resize / 100)
    lines=source=img=cv2.resize(img,(x,y))
    #ROI
    source = cv2.rectangle(source, (350,142), (650,420), (244,50,50), 1)
    x_0=142
    x_1=280
    y_0=350
    y_1=302
    source=source[x_0:x_0+x_1,y_0:y_0+y_1]

    h_min = np.array((255), np.uint8)    
    h_max = np.array((255), np.uint8) 
    source=cv2.inRange(source, h_min, h_max)
    contours = cv2.findContours(source, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
    x_line_2_ver=x_line_1_ver = int (115+img.shape[1]/2)
    y_line_1_ver = int (-100+img.shape[0]/2)
    y_line_2_ver = int (100+img.shape[0]/2)

    x_line_1_hor = int (-115+img.shape[1]/2)
    y_line_2_hor=y_line_1_hor = int (35+img.shape[0]/2)
    x_line_2_hor = int (215+img.shape[1]/2)
  
    cv2.line(lines, (x_line_1_ver, y_line_1_ver), (x_line_2_ver, y_line_2_ver), (255, 255, 255), thickness=1)
    cv2.line(lines, (x_line_1_hor, y_line_1_hor-10), (x_line_2_hor, y_line_2_hor-10), (255, 255, 255), thickness=1)

    distance="N/A"
    for c in contours:  
     ((x1, y1), radius) = cv2.minEnclosingCircle(c)
     if radius > 5:
      distance = math.sqrt((x_line_1_ver - (x1+y_0))**2 + (y_line_1_hor - (y1+x_0))**2)
      #print ("distance in pixels",round(distance,2))
      source=cv2.circle(lines, (int(x1)+y_0, int(y1)+x_0), 2,(150, 55, 55), 10)
    if contours!=(): 
        cv2.imshow("camera-" + str(number),lines)
        cv2.waitKey(1)
    else:
        #print ("not found")
        #cap.set(cv2.CAP_PROP_BUFFERSIZE, 3
        cv2.putText(lines, "camera-"+str(number)+" Laser beam was not found!", (20,20), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2)
        cv2.imshow("camera-" + str(number),lines)
        cv2.waitKey(1)
    return distance

def acquire_and_display_images(cam, number):
    sNodemap = cam.GetTLStreamNodeMap()
    node_bufferhandling_mode = PySpin.CEnumerationPtr(sNodemap.GetNode('StreamBufferHandlingMode'))
    node_newestonly = node_bufferhandling_mode.GetEntryByName('NewestOnly')

    node_newestonly_mode = node_newestonly.GetValue()
    node_bufferhandling_mode.SetIntValue(node_newestonly_mode)

    image_result = cam.GetNextImage(10)                
    image_data = image_result.GetNDArray()
    beam = image_processing(image_data, number)
    image_result.Release()
    return(beam)
    #cam.EndAcquisition()
           
def main():
    system = PySpin.System.GetInstance()
    version = system.GetLibraryVersion()
    cam_list = system.GetCameras()
    num_cameras = cam_list.GetSize()

    cam_list[0].Init()
    nodemap = cam_list[0].GetNodeMap()
    cam_list[0].BeginAcquisition()
    cam_list[1].Init()
    nodemap = cam_list[1].GetNodeMap()
    cam_list[1].BeginAcquisition()

    connection1=Connection.open_serial_port("COM4")
    connection2=Connection.open_serial_port("COM5")
    device_list1 = connection1.detect_devices()
    device_list2 = connection2.detect_devices()             
    print("Found {} devices".format(len(device_list1)))
    device_1_1 = device_list1[0]
    device_1_2 = device_list1[1]
    device_2_1 = device_list2[0]
    device_2_2 = device_list2[1]

    a=0
    start_time = time.time()
    dataset = pd.DataFrame({"beam_1": [],"beam_2": [],"mount_1_1": [],"mount_1_2": [],"mount_2_1": [],"mount_2_2": [],"time": []} )
    try:
        while 1:
            a+=1
            beam_1=acquire_and_display_images(cam_list[0],1)
            beam_2=acquire_and_display_images(cam_list[1],2)
            #print ("beam_1",beam_1,"beam_2",beam_2)
            try:
                mount_1_1=device_1_1.get_position() #print ("device_1_1", device_1_1.get_position())
                mount_1_2=device_1_2.get_position() #print ("device_1_2", device_1_2.get_position())
                mount_2_1=device_2_1.get_position() #print ("device_2_1", device_2_1.get_position())
                mount_2_2=device_2_2.get_position() #print ("device_2_2", device_2_2.get_position())
            except RequestTimeoutException:
#               print(err.details.reason)
                print ("time_error")
                mount_1_1=mount_1_2=mount_1_3=mount_1_4="N/A"

                
            times = time.time() - start_time
            data = [beam_1,beam_2, mount_1_1, mount_1_2, mount_2_1, mount_2_2, times]
            dataset.loc[a] = data
            print (dataset)
    except KeyboardInterrupt:
            dataset.to_excel('./dataset.xlsx')
main()


