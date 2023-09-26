import serial
import serial.tools.list_ports
import struct
import time
import numpy
import keyBoardInput



def findSerialPortByName(Name):
    available_ports = list(serial.tools.list_ports.comports())
    for port in available_ports:
        if Name in port.description:
            return port.device
    return None

        
        
ser = serial.Serial(findSerialPortByName('USB-SERIAL CH340'), 9600)

joystick_device = findSerialPortByName('Arduino Mega 2560')

if joystick_device!=None:
    serJoy = serial.Serial(joystick_device, 9600)




update_interval = 0.7
last_update_time = time.time()
data = []


while True:
    if joystick_device!=None:
        data = numpy.array(serJoy.readline().decode('utf-8').strip().split(' ')).astype(int)
    else:
        data = keyBoardInput.data




    data = numpy.append(data, 0)

    if time.time() - last_update_time >= update_interval:
        data[-1] = 1
        last_update_time = time.time()

    packed_data = b''
    for value in data:
        packed_data += struct.pack('B', value)
        
        
    print(data, end='\r')
    
    ser.write(packed_data)

    time.sleep(0.02)

    if ser.inWaiting() > 0:
        telemetry = struct.unpack("BBBB", ser.read(4))
        temp = telemetry[0]/5
        deep = telemetry[1] + telemetry[2]/100
        voltage = round(((3.3 * telemetry[3]/100) * 1.5), 2)
        print('temp ', temp, 'deep ', deep, ' ', voltage, end='\r')



