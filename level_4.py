import time 
import RPi.GPIO as GPIO
import threading
import urllib.request

#Geen Waarschuwingen en juiste schema voor pins
GPIO.setmode(GPIO.BCM) 
GPIO.setwarnings(False)

#GPIO pins motoren
motor1 = [2,3,4,17]
motor2 = [27,22,10,9]

#GPIO PINS sensoten en knoppen
sensorl = 14
sensorm = 15
sensorr = 18
knop = 26
knopl = 6
knopm = 19
knopr = 13
lichtRA = 5
lichtRV = 12
lichtLA = 25
lichtLV = 24

#Lichtrichting en richting begin waardes
lichtrichting = "vooruit"
richting = "vooruit"

#Standaardwaarde lichtknipperen
lichtknipper = True
lichtenaan = True

#Sequences
SeqVoorAchter1 = [[1,0,0,0],[1,1,0,0],[0,1,0,0],[0,1,1,0],[0,0,1,0],[0,0,1,1],[0,0,0,1],[1,0,0,1]]
SeqVoorAchter2 = [[0,0,0,1],[0,0,1,1],[0,0,1,0],[0,1,1,0],[0,1,0,0],[1,1,0,0],[1,0,0,0],[1,0,0,1]]

#Lengte van sequens en controle of beide even groot zijn
stepcountVoorAchter1 = len(SeqVoorAchter1)
stepcountVoorAchter2 = len(SeqVoorAchter2)
stepcountvoorAchter = 0
if (stepcountVoorAchter1 == stepcountVoorAchter2):
    stepcountVoorAchter = stepcountVoorAchter1

#Vertragingsvariabele voor motors
delay = 2/float(1000)

#pinnen van motoren op outputs zetten en op 0
for pin in motor1:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, 0)
for pin in motor2:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, 0)

#GPIO pinnen op inputs zetten   
GPIO.setup(sensorl, GPIO.IN)
GPIO.setup(sensorm, GPIO.IN)
GPIO.setup(sensorr, GPIO.IN)
GPIO.setup(knop, GPIO.IN, GPIO.PUD_UP)
GPIO.setup(knopl, GPIO.IN, GPIO.PUD_UP)
GPIO.setup(knopr, GPIO.IN, GPIO.PUD_UP)
GPIO.setup(knopm, GPIO.IN, GPIO.PUD_UP)

#GPIO pinnen op uitputs zetten
GPIO.setup(lichtRA,GPIO.OUT)
GPIO.setup(lichtRV,GPIO.OUT)
GPIO.setup(lichtLA,GPIO.OUT)
GPIO.setup(lichtLV,GPIO.OUT)

#Juiste lichtjes aan
def lichtjesuit () :
    GPIO.output(lichtRA, GPIO.LOW)
    GPIO.output(lichtRV, GPIO.LOW)
    GPIO.output(lichtLA, GPIO.LOW)
    GPIO.output(lichtLV, GPIO.LOW)

def lichtjesLinks() :
    GPIO.output(lichtRA, GPIO.LOW)
    GPIO.output(lichtRV, GPIO.LOW)
    GPIO.output(lichtLA, GPIO.HIGH)
    GPIO.output(lichtLV, GPIO.HIGH)

def lichtjesAan() :
    GPIO.output(lichtRA, GPIO.HIGH)
    GPIO.output(lichtRV, GPIO.HIGH)
    GPIO.output(lichtLA, GPIO.HIGH)
    GPIO.output(lichtLV, GPIO.HIGH)

def lichtjesRechts() :
    GPIO.output(lichtRA, GPIO.HIGH)
    GPIO.output(lichtRV, GPIO.HIGH)
    GPIO.output(lichtLA, GPIO.LOW)
    GPIO.output(lichtLV, GPIO.LOW)

#Lichtjes uitzetten
lichtjesuit()

def rij(motor, seq) :
    GPIO.output(motor[0], seq[0])
    GPIO.output(motor[1], seq[1])
    GPIO.output(motor[2], seq[2])
    GPIO.output(motor[3], seq[3])

def vooruit(step) :
    global motor1
    global motor2
    global lichtrichting
    #Beide motortjes een andere richting draaien
    rij(motor1, SeqVoorAchter1[step])
    rij(motor2, SeqVoorAchter2[step])
    lichtrichting = "vooruit"
    
def rechts(step):
    global motor1
    global motor2
    global lichtrichting
    #Beide motortjes dezelfde richting draaien
    rij(motor1, SeqVoorAchter1[step])
    rij(motor2, SeqVoorAchter1[step])
    lichtrichting = "rechts"

def links(step):
    global motor1
    global motor2
    global lichtrichting
    #Beide motortjes dezelfde richting draaien
    rij(motor2, SeqVoorAchter2[step])
    rij(motor1, SeqVoorAchter2[step])
    lichtrichting = "links"

def draaiwiel(richting, hoeveelheid):
    global delay
    global stepcountVoorAchter
    aantal = hoeveelheid * 256
    for step in range (0,aantal) :
        time.sleep(delay)                
        if (richting == "links") :
            links(step % stepcountVoorAchter)
        if (richting == "rechts") :
            rechts(step % stepcountVoorAchter)
        if (richting == "vooruit") :
            vooruit(step % stepcountVoorAchter)

#Rijden van auto
def rijden():
    step = 0
    kruispuntGehad = False
    while True:
        #Kruispunt gedetecteerd
        if (not GPIO.input(sensorl) and not GPIO.input(sensorm) and not GPIO.input(sensorr)) :
            #Controleren op tweede keer kruispunt
            if (kruispuntGehad) :
                #Tweede keer kruispunt dus stoppen
                urllib.request.urlopen("http://127.0.0.1:3000/bestemmingbereikt/").read()
                break
            else :
                urllib.request.urlopen("http://127.0.0.1:3000/kruispuntgevonden/").read()
                if (richting == "links") :
                    #Handmatige bocht op kruising
                    draaiwiel("vooruit", 3)
                    draaiwiel("links", 8)
                    draaiwiel("vooruit", 2)
                if (richting == "vooruit") :
                    #Handmatige bocht op kruising
                    draaiwiel("vooruit", 2)
                if (richting == "rechts") :
                    #Handmatige bocht op kruising
                    draaiwiel("vooruit", 3)
                    draaiwiel("rechts", 8)
                    draaiwiel("vooruit", 2)
                urllib.request.urlopen("http://127.0.0.1:3000/onderwegnaarbestemming/").read()
                kruispuntGehad = True
        #Naar links gedetecteerd
        elif (not GPIO.input(sensorl) and GPIO.input(sensorr)) :
            links(step)
        #Naar recht gedetecteerd
        elif (GPIO.input(sensorl) and not GPIO.input(sensorr)) :
            rechts(step)
        #Niks gedetecteerd
        else  :
            vooruit(step)
        if(step == stepcountVoorAchter - 1):
                step = 0
        else :
                step = step + 1
        time.sleep(delay)

#Licht laten knipperen
def knipper() :
    global lichtrichting
    global lichtknipper
    global lichtenaan
    while lichtenaan:
        if (lichtknipper):
            lichtknipper = False
            if (lichtrichting == "links"):
                lichtjesLinks()
            if (lichtrichting == "rechts"):
                lichtjesRechts()
            if (lichtrichting == "vooruit"):
                lichtjesAan()
        else:
            lichtknipper = True
            lichtjesuit()
        time.sleep(1)

#Lichtknipper code apart laten draaien
lichtenknipperen = threading.Thread(target=knipper)
lichtenknipperen.start()

#Start code
urllib.request.urlopen("http://127.0.0.1:3000/wachtenopbestemming/").read()
while True:
    #Knop starten ingedrukt
    if (not GPIO.input(knop)) :
        kruispunt = False
        urllib.request.urlopen("http://127.0.0.1:3000/onderwegnaarkruispunt/").read()
        rijden()
        lichtenaan = False
        break
    #Knop rechts ingedrukt
    elif (not GPIO.input(knopr)) :
        richting = "rechts"
        lichtenknipperen = True
        lichtjesRechts()
        urllib.request.urlopen("http://127.0.0.1:3000/klaaromtestarten/").read()
    #Knop vooruit ingedrukt
    elif (not GPIO.input(knopm)) :
        richting = "vooruit"
        lichtenknipperen = True
        lichtjesAan()
        urllib.request.urlopen("http://127.0.0.1:3000/klaaromtestarten/").read()
    #Knop links ingedrukt
    elif (not GPIO.input(knopl)) : 
        richting = "links"
        lichtenknipperen = True
        lichtjesLinks()
        urllib.request.urlopen("http://127.0.0.1:3000/klaaromtestarten/").read()
    lichtrichting = richting
    time.sleep(0.1)