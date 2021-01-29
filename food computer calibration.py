from atlas_i2c import atlas_i2c

sensor_address = 99
pH_sensor = atlas_i2c.AtlasI2C()
pH_sensor.set_i2c_address(sensor_address)

reading = pH_sensor.query("cal,low,4.01", processing_delay=1500)

pH = reading.data
check = reading.status_code
print(check)

pH = round(float(pH.decode("utf-8")),1)
print(pH)
