import time
from grove.grove_light_sensor_v1_2 import GroveLightSensor
from grove.grove_relay import GroveRelay
import seeed_dht
from grove.grove_moisture_sensor import GroveMoistureSensor
from firebase import firebase

dht11_sensor = seeed_dht.DHT("11", 5)
light_sensor = GroveLightSensor(2)
moisture_sensor = GroveMoistureSensor(0)
motor = GroveRelay(16)
thresh = 30


def automate() :
    watered = False
    if not watered :   
        while True :
            moisture = moisture_sensor.moisture
            moisture = moisture*100/1023
       
           
            if moisture > thresh :
                motor.off()
                print ('motor is off')
                watered = True
                break
                    
                    
            else :
                motor.on()
                print('motor is on')
                
            time.sleep(1)
 
firebase = firebase.FirebaseApplication('https://iot-smart-garden-44a0f.firebaseio.com/', None)

def main ():
    while True :
        motor_state= firebase.get('/iot-smart-garden-44a0f','motor_state')
        update = firebase.get('/iot-smart-garden-44a0f','update')
        pi_state= firebase.get('/iot-smart-garden-44a0f','pi_state')
        
        if (pi_state == unicode("0")) :
            motor.off()
            break
        moisture = moisture_sensor.moisture
        moisture = moisture*100/1023
        light = light_sensor.light
        light=light*100/1023
        humi, temp = dht11_sensor.read()
        print('humidity {}%, temperature {}*C \n'.format( humi, temp))
        print('light {}%, moisture {}% \n'.format( light, moisture))
        
        if (update == unicode("1")):
            print ("updating database")
            firebase.put('iot-smart-garden-44a0f', 'temperature', str(temp))
            firebase.put('iot-smart-garden-44a0f', 'humidity', str(humi))
            firebase.put('iot-smart-garden-44a0f', 'light', str(light))
            firebase.put('iot-smart-garden-44a0f', 'moisture', str(moisture))
            firebase.put('iot-smart-garden-44a0f', 'update', str(0))
        
        if (motor_state == unicode("1")) :
            print ("motor mode on")
            motor.on()
        if (motor_state == unicode("2")) :
            print ("motor automatic control")
            automate()
        
        

if __name__ == '__main__':
    main()