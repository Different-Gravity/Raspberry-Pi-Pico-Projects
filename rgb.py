# import modules
########################################
from machine import Pin, PWM, ADC
from time import sleep

# set up pins
########################################
red_rgb = PWM(Pin(20), freq=1000)  
green_rgb = PWM(Pin(19), freq=1000)  
blue_rgb = PWM(Pin(18), freq=1000) 

modes = ["Red", "Green", "Blue"]
currentMode = ""

redval = 0
greenval = 0
blueval = 0

red = Pin(7, Pin.OUT)
green = Pin(8, Pin.OUT)
blue = Pin(9, Pin.OUT)

redstate = False
greenstate = False
bluestate = False

pot = ADC(Pin(26))

button = Pin(22, Pin.IN, Pin.PULL_UP)
# button pressed button.value() == 0

duty_step = 129 

counter = 0

prev_state = 1
buttonState = 0

# FUNCTIONS
#########################################

# Function to set RGB LED color
# Assume input is 0 to 255
# 100% of cycle (full brightness) is 65535 (255 * 257)
def set_color(r, g, b):
    red_rgb.duty_u16(r*257) # Red intensity
    green_rgb.duty_u16(g*257)  # Green intensity
    blue_rgb.duty_u16(b*257)  # Blue intensity

def map_adc_to_PWM(value, in_min=0, in_max=65535, out_min=0, out_max=255):
    return int((value - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)


# MAIN CODE
#########################################

#assign initial values
red.off()
green.off()
blue.off()

set_color(redval, greenval, blueval)

while True:

    #add to counter when button is pressed
    buttonState = button.value()


    if (buttonState == 0 and prev_state == 1):
        counter = counter + 1
        sleep(0.2)  # debounce delay

    
    if counter == 3:
        counter = 0

    prev_state = buttonState

    #assign current mode based on counter value
    currentMode = modes[counter]

    #check potentiometer value and map to PWM range
    pot_value = map_adc_to_PWM(pot.read_u16())  # Read the potentiometer value (0-65535)
    PWM = (pot_value)

    #PWM value limits
    if PWM <= 20:
        PWM = 0

    if PWM >= 255:
        PWM = 255

    #button press logic to set color values based on current mode
    if currentMode == "Red":
        greenstate = False
        red.on()
        green.off()
        blue.off()

        if redstate == False and PWM >= redval:
            redstate = True
            
        if redstate == True:
            redval = int(PWM)
            set_color(redval, greenval, blueval)


    if currentMode == "Green":
        bluestate = False
        green.on()
        red.off()
        blue.off()

        if greenstate == False and PWM >= greenval:
            greenstate = True
           

        if greenstate == True:
            greenval = int(PWM)
            set_color(redval, greenval, blueval)

    if currentMode == "Blue":
        greenstate = False
        blue.on()
        red.off()
        green.off()

        if bluestate == False and PWM >= blueval:
            bluestate = True
            

        if bluestate == True:
            blueval = int(PWM)
            set_color(redval, greenval, blueval)

