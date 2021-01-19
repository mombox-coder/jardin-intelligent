#importer les bibliotheques necessaires au temps, capteurs, actionneurs et database
import time
from grove.grove_light_sensor_v1_2 import GroveLightSensor
from grove.grove_relay import GroveRelay
import seeed_dht
from grove.grove_moisture_sensor import GroveMoistureSensor
from firebase import firebase
from grove.display.jhd1802 import JHD1802

#définir les pins de chaque capteur/actionneur
lcd = JHD1802()
dht_sensor = seeed_dht.DHT("11", 5)
light_sensor = GroveLightSensor(2)
moisture_sensor = GroveMoistureSensor(0)
motor = GroveRelay(16)
thresh = 30

firebase = firebase.FirebaseApplication('https://iot-smart-garden-44a0f.firebaseio.com/', None) #définir l'URL de la base de donnée en temps réel
#communiquer à travers l'écran LCD que le système démarre
lcd.setCursor(0, 0)
lcd.write('hello')
lcd.setCursor(1, 0)
lcd.write('updating db')

#définir la fonction qui va être utilisé pendant le mode automatique
def automate() :
    watered = False
    if not watered :   
        while True :
            moisture = moisture_sensor.moisture
            moisture = moisture*100/1023
            
           
            if moisture > thresh :
                lcd.setCursor(1, 0)
                lcd.write('stopped     ')
                motor.off()
                watered = True
                break                    
                    
            else :
                lcd.setCursor(1, 0)
                lcd.write('watering')
                motor.on()

def main ():
    initTime = time.time()
    
    while True :
        #extraction des valeurs des capteurs à partir de la base de données en temps réel
        motor_state= firebase.get('/iot-smart-garden-44a0f','motor_state')
        update = firebase.get('/iot-smart-garden-44a0f','update')
        pi_state= firebase.get('/iot-smart-garden-44a0f','pi_state')
        print ("received data in")
        print (int(time.time()-initTime))
        initTime= time.time()
        
        #si on clique sur le bouton "arrêt" dans l'application mobile, le système s'arrête
        if (pi_state == unicode("0")) :
            motor.off()
            lcd.setCursor(0, 0)
            lcd.write('bye bye    ')
            lcd.setCursor(1, 0)
            lcd.write('sleeping     ')
            break
            
        moisture = moisture_sensor.moisture
        moisture = moisture*100/1023
        light = light_sensor.light
        light=light*100/1023
        humidity, temp = dht_sensor.read()
        print('humidity {}%, temperature {}*C \n'.format( humidity, temp))
        print('light {}%, moisture {}% \n'.format( light, moisture))
        
        #si on clique sur le bouton "rafraîchir", on extrait les nouvelles valeurs des capteurs stockées dans la base de donnée
        if (update == unicode("1")):
            print ("updating database")
            firebase.put('iot-smart-garden-44a0f', 'temperature', str(temp))
            firebase.put('iot-smart-garden-44a0f', 'humidity', str(humidity))
            firebase.put('iot-smart-garden-44a0f', 'light', str(light))
            firebase.put('iot-smart-garden-44a0f', 'moisture', str(moisture))
            firebase.put('iot-smart-garden-44a0f', 'update', str(0))
        
        #si on clique sur le mode On, l'arrosage démarre
        if (motor_state == unicode("1")) :
            motor.on()
            lcd.setCursor(0, 0)
            lcd.write('mode on  ')
            lcd.setCursor(1, 0)
            lcd.write('watering       ')           
            
        #si on clique sur le mode Auto, on active l'arrosage automatique défini précedemment dans la fonction automate()    
        elif (motor_state == unicode("2")) :
            lcd.setCursor(0, 0)
            lcd.write('mode auto')
            automate()
        #si on clique sur le bouton Off, on arrête l'arrosage
        else :           
            motor.off()
            lcd.setCursor(0, 0)
            lcd.write('mode off  ')
            lcd.setCursor(1, 0)
            lcd.write('stopped      ')  
        
        

if __name__ == '__main__':
    main()
