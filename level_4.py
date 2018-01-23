import time 
import RPi.GPIO as GPIO 
import threading

GPIO.setmode(GPIO.BCM) 
GPIO.setwarnings(False)

motor1 = [2,3,4,17]
motor2 = [27,22,10,9]

sensorl = 14
sensorm = 15
sensorr = 18

knop = 26
knopl = 13
knopr = 6
knopm = 19

##Seq voor en achter uit
SeqVoorAchter1 = [[1,0,0,0],[1,1,0,0],[0,1,0,0],[0,1,1,0],[0,0,1,0],[0,0,1,1],[0,0,0,1],[1,0,0,1]]
SeqVoorAchter2 = [[0,0,0,1],[0,0,1,1],[0,0,1,0],[0,1,1,0],[0,1,0,0],[1,1,0,0],[1,0,0,0],[1,0,0,1]]

delay = 2/float(1000)

for pin in motor1:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, 0)

for pin in motor2:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, 0)
    
GPIO.setup(sensorl, GPIO.IN)
GPIO.setup(sensorm, GPIO.IN)
GPIO.setup(sensorr, GPIO.IN)
GPIO.setup(knop, GPIO.IN, GPIO.PUD_UP)
GPIO.setup(knopl, GPIO.IN, GPIO.PUD_UP)
GPIO.setup(knopr, GPIO.IN, GPIO.PUD_UP)
GPIO.setup(knopm, GPIO.IN, GPIO.PUD_UP)
    
stepcountVoorAchter1 = len(SeqVoorAchter1)
stepcountVoorAchter2 = len(SeqVoorAchter2)

stepcountvoorAchter = 0

if (stepcountVoorAchter1 == stepcountVoorAchter2):
    stepcountVoorAchter = stepcountVoorAchter1
    
def rij(motor, seq) :
    GPIO.output(motor[0], seq[0])
    GPIO.output(motor[1], seq[1])
    GPIO.output(motor[2], seq[2])
    GPIO.output(motor[3], seq[3])

def vooruit(step) :
    global motor1
    global motor2
    rij(motor1, SeqVoorAchter1[step])
    rij(motor2, SeqVoorAchter2[step])

def achteruit(step) :
    global motor1
    global motor2
    rij(motor1, SeqVoorAchter2[step])
    rij(motor2, SeqVoorAchter1[step])
    
def rechts(step):
    global motor1
    global motor2
    rij(motor1, SeqVoorAchter1[step])
    rij(motor2, SeqVoorAchter1[step])

def links(step):
    global motor1
    global motor2
    rij(motor2, SeqVoorAchter2[step])
    rij(motor1, SeqVoorAchter2[step])

def rondjewiel(richting, hoeveelheid):
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
        

kruispunt = False

step = 0

richting = "vooruit"

def start():
    global step
    global kruispunt
    while True:
        if (not GPIO.input(sensorl) and not GPIO.input(sensorm) and not GPIO.input(sensorr)) :
            if (kruispunt) :
                break
            else :
                if (richting == "links") :
                    rondjewiel("vooruit", 3)
                    rondjewiel("links", 8)
                    rondjewiel("vooruit", 2)
                if (richting == "vooruit") :
                    rondjewiel("vooruit", 2)
                if (richting == "rechts") :
                    rondjewiel("vooruit", 3)
                    rondjewiel("rechts", 8)
                    rondjewiel("vooruit", 2)
                kruispunt = True
        elif (not GPIO.input(sensorl) and GPIO.input(sensorr)) :
            links(step)
        elif (GPIO.input(sensorl) and not GPIO.input(sensorr)) :
            rechts(step)
        else  :
            vooruit(step)
        if(step == stepcountVoorAchter - 1):
                step = 0
        else :
                step = step + 1
        time.sleep(delay)

while True:
    if (not GPIO.input(knop)) :
        start()
        break
    if (not GPIO.input(knopr)) :
        richting = "rechts"
    if (not GPIO.input(knopm)) :
        richting = "vooruit"
    if (not GPIO.input(knopl)) : 
        richting = "links"
    time.sleep(0.1)