import serial
import serial.tools.list_ports
import struct
import time
import numpy
import keyboard_input_handler
import json
import threading


def find_serial_port_by_name(name):
    available_ports = list(serial.tools.list_ports.comports())
    for port in available_ports:
        if name in port.description:
            return port.device
    return None


ser = serial.Serial(find_serial_port_by_name('USB-SERIAL CH340'), 9600)
joystick_arduino_name = 'Arduino Mega 2560'
joystick_device = find_serial_port_by_name(joystick_arduino_name)
data = numpy.zeros(6)
fresh_rate = 0.02

if joystick_device is not None:
    ser_joystick = serial.Serial(joystick_device, 9600)


def write():
    global data, joystick_device, ser_joystick, fresh_rate
    telemetry_update_interval = 0.5
    last_update_time = time.time()
    
    while True:
        try:
            
            if joystick_device is not None:
                data = numpy.array(ser_joystick.readline().decode('utf-8').strip().split(' ')).astype(int)
            else:
                data = keyboard_input_handler.data
                
            data = numpy.append(data, 0)
            if time.time() - last_update_time >= telemetry_update_interval:
                data[-1] = 1
                last_update_time = time.time()
                if joystick_device is None and find_serial_port_by_name(joystick_arduino_name) is not None:
                    raise Exception("Joystick connected!")
                                   
            ser.write(struct.pack('BBBBBB', *data))
            time.sleep(fresh_rate)
            
        except ValueError:
            print("Joystick disconnected!")
            ser_joystick.close()
            joystick_device = None
            continue
            
        except Exception as inner_error:
            print(inner_error)

            joystick_device = find_serial_port_by_name(joystick_arduino_name)
            if joystick_device is not None:
                ser_joystick = serial.Serial(joystick_device, 9600)


def read():
    global data, fresh_rate
    termination_character = b'\n'
    
    while True:
        try:
            
            if ser.inWaiting() > 0:  
                received_data = b''    
                while termination_character not in received_data:
                    received_data += ser.read(1)            
    
                telemetry_raw = struct.unpack("BBBB", ser.read(4))
                        
                telemetry = {
                    "temperature": float(telemetry_raw[0]/5),
                    "deep": float(telemetry_raw[1] + telemetry_raw[2]/100),
                    "voltage": round(((3.3 * telemetry_raw[3]/100) * 1.5), 2),
                    "engine_max_power ": int(data[3]),
                    "flashlight_brightness: ": int(data[4]),
                    "buoyancy": ("up" if data[2] == 0 else "down" if data[2] == 2 else "neutral")
                }
                
                with open("telemetry.js", "w") as js_file:
                    js_file.write(f"var myObject = {telemetry};")
                    
            time.sleep(fresh_rate)
                    
        except Exception as inner_error:
            print(inner_error)
            
            
                
                
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
        ser_joystick.close()