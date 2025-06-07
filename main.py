import math, time
 
# importing cv2 
import cv2

import numpy as np

import serial

def getPoint(pos,angle,dist):
    angle = math.radians(angle)
    return [pos[0]+math.cos(angle)*dist, pos[1]+math.sin(angle)*dist]

# black blank image
image = np.zeros(shape=[500, 500, 3], dtype=np.uint8)

window_name = 'Image'


# Configure the serial port
ser = serial.Serial(
    port='/dev/ttyUSB0',
    baudrate=9600,
    timeout=1
)

data_points = np.array([[0,0],[0,0],[0,0],[0,0],[0,0],[0,0]], np.int32)

point_vel = [0.0,0.0,0.0,0.0,0.0,0.0]

point_acc = [0.0,0.0,0.0,0.0,0.0,0.0]

point_dist = [50.0,50.0,50.0,50.50,50.50,50.0]

cv2.imshow(window_name, image)

old_time = time.time()

received_data = []

try:
    while True:
        # Receive data
        image = np.zeros(shape=[500, 500, 3], dtype=np.uint8)
        if ser.in_waiting > 0:
            received_data = ser.readline().decode('utf-8').strip()
            received_data = received_data.split(',')
            received_data.remove('')
            #print(f"Received: {received_data}")
        for i in range(0,len(received_data)):
            received_data[i]=int(float(received_data[i]))
            if received_data[i] == 0:
                received_data[i] = 50

            point_acc[i] = (-50+received_data[i]) + (received_data[i]-point_dist[i])
            point_vel[i] += point_acc[i]*0.01
            point_vel[i] *= 0.9
            point_dist[i] += point_vel[i]
            data_points[i] = getPoint([250,250],i*60,point_dist[i]*3)
            cv2.circle(image, tuple(data_points[i]), 5, (255,255,255), -1)

        #old_time = time.time()
            
        image = cv2.polylines(image, [data_points], True, (255,255,255), 1)
        cv2.imshow(window_name, image)
        cv2.waitKey(1)

except KeyboardInterrupt:
    ser.close()
    print("Serial port closed.")
