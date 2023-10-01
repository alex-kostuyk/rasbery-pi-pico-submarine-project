from machine import Pin, UART, I2C, PWM, reset
import struct
import machine
import time
import BME280

#MAX485 values
uart = UART(0, baudrate=9600, tx=Pin(0), rx=Pin(1))
uart.init(bits=16, parity=None, stop=1)
Pin(2, Pin.OUT).value(1)
# value(0) to read data value(1) to write
max485_read_write_pin = Pin(3, Pin.OUT)

#BME280 values
Pin(18, Pin.OUT).value(1)
sda=Pin(16)
scl=Pin(17)
i2c=machine.I2C(0,sda=sda, scl=scl, freq=200000)
bme = BME280.BME280(i2c=i2c)

#analog pins
floating_module_position = machine.ADC(26)
battery_voltage = machine.ADC(27)

#light pins
flashlight = PWM(Pin(8))
flashlight.freq(500)
LED = Pin(25, Pin.OUT)


#engine value
max_freq = 6400
min_freq = 3500
#10 back 11 left 12 right
engine_pins = [10, 11, 12]
engines = [PWM(Pin(pin, Pin.OUT)) for pin in engine_pins]
#esc init
for engine in engines:
    engine.freq(50)
    engine.duty_u16(max_freq)

time.sleep(1)

for engine in engines:
    engine.freq(50)
    engine.duty_u16(min_freq)

time.sleep(1)





def power_percentage_to_pwm_signal(power_percent):
    return int(min_freq + (max_freq - min_freq) * (power_percent / 100.0))


DEFAULT_DATA = [50,50,1,50,50]
data = []
power = [0]*3

while True:
    
    if uart.any():
        data = struct.unpack("BBBBBB",  uart.read())
        flashlight.duty_u16(int(655.36 * data[4]))
        print("asdas")
        #send telemetry
        if data[-1] == 1:
            max485_read_write_pin.value(1)
            LED.value(1)
            
            temp = int(bme.read_temperature()/20)
            deep = (float(bme.pressure)-1005)/100
            voltage = int((battery_voltage.read_u16()/65535)*100)
            uart.write(b'\n'+struct.pack("BBBB", temp, int(deep), int((deep % 1) * 100), voltage))    
            time.sleep(0.02)
            LED.value(0)
            max485_read_write_pin.value(0)
                
                
    else:
        data = DEFAULT_DATA
        
    power[2] = ((data[1]-50 if data[1]> 50 else 0) + (data[0]-50 if data[0]> 50 else 0))* data[3]/100
    power[1] = ((50 - data[1] if data[1]< 50 else 0) + (data[0]-50 if data[0]> 50 else 0))* data[3]/100
    power[0] = (50 - data[0] if data[0]< 50 else 0)* data[3]/100
        
    for i in range(3):
        engines[i].duty_u16(power_percentage_to_pwm_signal(power[i]))
            
    time.sleep(0.02)

