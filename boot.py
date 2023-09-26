from machine import Pin, UART, I2C, PWM
import struct
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

#analog pins
floating_module_position = machine.ADC(26)
battery_voltage = machine.ADC(27)

#pwm pins
light_pwm =PWM(Pin(8))
light_pwm.freq(500)

LED = Pin(25, Pin.OUT)


bme = BME280.BME280(i2c=i2c)

while True:
    
    LED.toggle()
    if uart.any():
        data = struct.unpack("BBBBBB",  uart.read())

        light_pwm.duty_u16(int(655.36 * data[4]))
        
        #send telemetry
        if data[-1] == 1:
            max485_read_write_pin.value(1)
            
            temp = int(bme.read_temperature()/20)
            deep = (float(bme.pressure)-1005)/100
            voltage = int((battery_voltage.read_u16()/65535)*100)

            
            uart.write(struct.pack("BBBB", *[temp, int(deep), int((deep % 1) * 100), voltage]))
            
            time.sleep(0.02)
            LED.toggle()
            max485_read_write_pin.value(0)
            
            
        
        
    time.sleep(0.02)