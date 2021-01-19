'''importer les bibliotheques necessaires au temps, capteurs,
actionneurs et database'''
import time
from grove.grove_light_sensor_v1_2 import GroveLightSensor
from grove.grove_relay import GroveRelay
import seeed_dht
from grove.grove_moisture_sensor import GroveMoistureSensor
from firebase import firebase
from grove.display.jhd1802 import JHD1802

'''definir les pins de chaque capteur/actionneur'''
lcd = JHD1802()
dht_capteur = seeed_dht.DHT("11", 5)
capteur_lumiere = GroveLightSensor(2)
capteur_hum_sol = GroveMoistureSensor(0)
motor = GroveRelay(16)
seuil = 30

firebase =
firebase.FirebaseApplication('https://iot-smart-garden-44a0f.firebaseio.com/')
'''definir l'URL de la base de donnee en temps reel et
communiquer a travers l'ecran LCD que le systeme demarre'''
lcd.setCursor(0, 0)
lcd.write('Bonjour')
lcd.setCursor(1, 0)
lcd.write('Maj du Cloud...')

'''definir la fonction qui va etre utilise pendant le mode automatique'''
def automatique() :
    irrigue = False
    if not irrigue :   
        while True :
            hum_sol = capteur_hum_sol.moisture
            hum_sol = hum_sol*100/1023
            if hum_sol > seuil :
                lcd.setCursor(1, 0)
                lcd.write('stopped')
                motor.off()
                irrigue = True
                break                    
            else :
                lcd.setCursor(1, 0)
                lcd.write('watering')
                motor.on()
def main ():
    temps_init = time.time()
    while True :
        '''extraction des ordres a partir de la base de donnees en temps reel'''
        etat_moteur= firebase.get('/iot-smart-garden-44a0f','etat_moteur')
        rafraichir = firebase.get('/iot-smart-garden-44a0f','rafraichir')
        etat_pi= firebase.get('/iot-smart-garden-44a0f','etat_pi')
        print ("donnees recues en ")
        print (int(time.time()-temps_init))
        temps_init= time.time()
        
        '''si on clique sur le bouton "eteindre" dans l'application mobile,
        le systeme s'arrete'''
        if (etat_pi == unicode("0")) :
            motor.off()
            lcd.setCursor(0, 0)
            lcd.write('bye bye')
            lcd.setCursor(1, 0)
            lcd.write('sleeping')
            break
            
        hum_sol = capteur_hum_sol.moisture
        hum_sol = hum_sol*100/1023
        lumiere = capteur_lumiere.light
        lumiere=lumiere*100/1023
        humidite, temperature = dht_capteur.read()
        print('humidite {}%, temperature {}*C \n'.format( humidite, temperature))
        print('lumiere {}%, humidite du sol {}% \n'.format( lumiere, hum_sol))
        
        '''si on clique sur le bouton "rafraichir", on remplace les
        anciennes valeurs des capteurs stockees dans la base de donnee
        par des nouvelles'''
        if (rafraichir == unicode("1")):
            firebase.put('iot-smart-garden-44a0f', 'temperature',
            str(temperature))
            firebase.put('iot-smart-garden-44a0f', 'humidite', str(humidite))
            firebase.put('iot-smart-garden-44a0f', 'lumiere', str(lumiere))
            firebase.put('iot-smart-garden-44a0f', 'humidite du sol',
            str(hum_sol))
            firebase.put('iot-smart-garden-44a0f', 'rafraichir', str(0))
        
        '''si on clique sur le mode On, l'arrosage demarre et on en informe 
        l'utilisateur via l'ecran LCD'''
        if (etat_moteur == unicode("1")) :
            motor.on()
            lcd.setCursor(0, 0)
            lcd.write('mode on')
            lcd.setCursor(1, 0)
            lcd.write('watering')           
            
        '''si on clique sur le mode Auto, on active l'arrosage automatique
        defini precedemment dans la fonction automate()'''
        elif (etat_moteur == unicode("2")) :
            lcd.setCursor(0, 0)
            lcd.write('mode auto')
            automatique()
        '''si on clique sur le bouton Off, on arrete l'arrosage et on en 
        informe l'utilisateur via l'ecran LCD'''
        else :           
            motor.off()
            lcd.setCursor(0, 0)
            lcd.write('mode off')
            lcd.setCursor(1, 0)
            lcd.write('stopped')  
        
if __name__ == '__main__':
    main()
