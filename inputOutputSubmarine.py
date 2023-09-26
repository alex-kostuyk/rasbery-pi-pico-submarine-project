import serial
import struct
import time
import numpy

ser = serial.Serial('COM9', 9600)
serJoy = serial.Serial('COM5', 9600)

update_interval = 0.7
last_update_time = time.time()


while True:
    data = numpy.array(serJoy.readline().decode('utf-8').strip().split(' ')).astype(int)

    data = numpy.append(data, 0)

    if time.time() - last_update_time >= update_interval:
        data[-1] = 1
        last_update_time = time.time()

    packed_data = b''
    for value in data:
        packed_data += struct.pack('B', value)

    # Send the packed data
    ser.write(packed_data)

    time.sleep(0.02)

    # Receive and print telemetry
    if ser.inWaiting() > 0:
        telemetry = struct.unpack("BBBB", ser.read(4))
        temp = telemetry[0]/5
        deep = telemetry[1] + telemetry[2]/100
        voltage = round(((3.3 * telemetry[3]/100) * 1.5), 2)
        print('temp ', temp, 'deep ', deep, ' ', voltage, end='\r')



