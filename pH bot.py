from Adafruit_IO import Client, Feed
import time
from adafruit_motorkit import MotorKit
from atlas_i2c import atlas_i2c

io_key = "94921b4b90264ebbb2b0fc9a08137e9e"
io_username = "reginius214"

aio = Client(io_username, io_key)

pump_button = aio.feeds('berlin-pump')
toggle = aio.feeds('berlin-toggle')
slider = aio.feeds('berlin-dosage')
pH_high_point = aio.feeds('berlin-ph-high')
pH_low_point = aio.feeds('berlin-ph-low')


pump = MotorKit(address = 0x61)
sensor_address = 1
pH_sensor = atlas_i2c.AtlasI2C()
pH_sensor.set_i2c_address(sensor_address)
reading = pH_sensor.query("R", processing_delay=1500)

update_reading = 10.0
reading_timer = time.time()


while True:
    time_now = time.time()
    
    if time_now - reading_timer >= update_reading:
        reading = pH_sensor.query("R",  processing_delay=1500)
        pH = reading.data
        pH = round(float(pH.decode("utf-8")),1)
        print(pH)
        toggle_value = aio.receive(toggle.key)
        mode = toggle_value.value
        slider_value = aio.receive(slider.key)
        volume = slider_value.value
        
        if mode == "Manual":
            button_value = aio.receive(pump_button.key)
            result = button_value.value
            if result == "1":
                pump.motor1.throttle = 1.0
                time.sleep(int(volume))
                pump.motor1.throttle = 0
       
        elif mode == "Auto":
            low_point = aio.receive(pH_low_point.key)
            low_point_value= float(low_point.value)
            high_point = aio.receive(pH_high_point.key)
            high_point_value= float(high_point.value)
            
            if pH < float(low_point_value):
                pump.motor1.throttle = 1.0
                time.sleep(float(volume))
                pump.motor1.throttle = 0
                if pH > float(high_point_value):
                    pump.motor1.throttle = 1.0
                    time.sleep(float(volume))
                    pump.motor1.throttle = 0

        reading_timer = time.time()
    time.sleep (0.5)

          
           

    
    
    
    
