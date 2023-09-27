import serial
import serial.tools.list_ports
import struct
import time
import numpy
import keyBoardInput
import json
import threading

def findSerialPortByName(Name):
    available_ports = list(serial.tools.list_ports.comports())
    for port in available_ports:
        if Name in port.description:
            return port.device
    return None

ser = serial.Serial(findSerialPortByName('USB-SERIAL CH340'), 9600)
joystick_device = findSerialPortByName('Arduino Mega 2560')
data = numpy.zeros(6)

if joystick_device!=None:
    serJoy = serial.Serial(joystick_device, 9600)
    
def write():
    global data
    update_interval = 0.7
    last_update_time = time.time()
    
    while True:
        try:
            if joystick_device!=None:
                data = numpy.array(serJoy.readline().decode('utf-8').strip().split(' ')).astype(int)
            else:
                data = keyBoardInput.data
                
            data = numpy.append(data, 0)
            if time.time() - last_update_time >= update_interval:
                data[-1] = 1
                last_update_time = time.time()
                if joystick_device==None and findSerialPortByName('Arduino Mega 2560') != None:
                    raise Exception("Joystick connected!")
                                   
            ser.write(struct.pack('BBBBBB', *data))
            time.sleep(0.02)
            
        except Exception as error:
            print(error)
        
def read():
    global data
    
    while True:
        if ser.inWaiting() > 0:     
            telemetry_raw = struct.unpack("BBBB", ser.read(4))
                
            telemetry = {
                "temperature": float(telemetry_raw[0]/5),
                "deep": float(telemetry_raw[1] + telemetry_raw[2]/100),
                "voltage": round(((3.3 * telemetry_raw[3]/100) * 1.5), 2),
                "engine_max_power ": int(data[3]),
                "flashlight_brightness: ": int(data[4]),
                "buoyancy":("up" if data[2] == 0 else "down" if data[2] == 2 else "neutral")
            }
            
            with open("telemetry.json","w") as json_file:
                json.dump(telemetry, json_file)
            time.sleep(0.02)
        

try:
    read_thread = threading.Thread(target=read)
    write_thread = threading.Thread(target=write)

    read_thread.start()
    write_thread.start()
        
    read_thread.join()
    write_thread.join()
except Exception as error:
    print(error)
finally:
    ser.close()
    if joystick_device is not None:
        serJoy.close()
            

        
    
        
                    
                
   
        





