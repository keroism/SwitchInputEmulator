import pygame
import time
import numpy as np
import math
import client2
import serial
import argparse
import threading

parser = argparse.ArgumentParser('Client for sending controller commands to a controller emulator')
parser.add_argument('port')
args = parser.parse_args()


c = client2.client2(port=args.port, baudrate=19200,timeout=1)

axis_history = [0,0,0,0]
axis_invert = [1,-1,1,-1]
button_values = np.zeros(25)



def macro1_thread (c):
    global stop_threads
    macro_counter = 0
    print ("in macro1 thread")
#    while True: 
#        circles(c, 10)
#        if stop_threads: 
#            break  
    while True: 
#        teleport(c)
        #gotoEmptyArea(c) 
        #circles(c, 10)
#        if stop_threads: 
#            break      
        time.sleep(.4); print("Loop #{}".format(macro_counter))
        teleport(c)
        if stop_threads: 
            break           
        gotoBreader(c)
        if stop_threads: 
            break           
        getEggFromBreader(c)
        if stop_threads: 
            break         
        teleport(c)  
        gotoEmptyArea(c) 
        circles(c, 43)
        mashA(c, 40)
        macro_counter = macro_counter + 1
        if stop_threads: 
            break        

    c.send_cmd(c.LSTICK_CENTER) ; c.p_wait(0.1)


def macro2_thread (c):
    global stop_threads
    print ("in macro2 thread")
    teleport(c)
    gotoBreader(c)
    c.send_cmd(c.LSTICK_CENTER) ; c.p_wait(0.1)

def teleport(c):
    print("teleport")
    time.sleep(0.5)
    #Bring up menu
    c.send_cmd(c.BTN_X) ; time.sleep(0.1) ;  c.send_cmd(); time.sleep(0.8)
    #Select bottom left
    c.send_cmd(c.LSTICK_L); time.sleep(0.8); c.send_cmd(c.LSTICK_CENTER) ; time.sleep(0.1) 
    c.send_cmd(c.LSTICK_D); time.sleep(0.8); c.send_cmd(c.LSTICK_CENTER) ; time.sleep(0.1) 
    c.send_cmd(c.BTN_A); time.sleep(0.1) ;  c.send_cmd();
    #wait for map to load and select location
    time.sleep(2)
    c.send_cmd(c.BTN_A) ; time.sleep(0.1) ;  c.send_cmd(); time.sleep(1)
    c.send_cmd(c.BTN_A) ; time.sleep(0.1) ;  c.send_cmd(); 
    time.sleep(5)
    return True

def gotoBreader(c):
    print("goto_breader")
    c.send_cmd(c.RSTICK_R) ; c.p_wait(2) ;  c.send_cmd(c.RSTICK_CENTER) ; time.sleep(0.1)  
    c.send_cmd(c.LSTICK_U) ; c.p_wait(0.5) ;  c.send_cmd(c.LSTICK_CENTER) ; time.sleep(0.1)  
    c.send_cmd(c.LSTICK_R) ; c.p_wait(0.5) ;  c.send_cmd(c.LSTICK_CENTER) ; time.sleep(0.1)  
    c.send_cmd(c.BTN_A) ; time.sleep(0.1) ;  c.send_cmd() ; time.sleep(0.1)  
    return True

def gotoEmptyArea(c):
    print("gotoEmptyArea")
    c.send_cmd(c.RSTICK_R) ; time.sleep(.25) ;  c.send_cmd(c.RSTICK_CENTER) ; time.sleep(0.1)  
    c.send_cmd(c.LSTICK_U) ; time.sleep(1) ;  c.send_cmd(c.LSTICK_CENTER) ; time.sleep(0.1)  
    c.send_cmd(c.LSTICK_R) ; time.sleep(1.5) ;  c.send_cmd(c.LSTICK_CENTER) ; time.sleep(0.1)  
    c.send_cmd(c.BTN_A) ; time.sleep(0.1) ;  c.send_cmd() ; time.sleep(0.1)  
    return True

def gotoEmptyArea2(c):
    print("gotoEmptyArea")
    c.send_cmd(c.RSTICK_R) ; time.sleep(.3) ;  c.send_cmd(c.RSTICK_CENTER) ; time.sleep(0.1)  
    c.send_cmd(c.LSTICK_U) ; time.sleep(0.4) ;  c.send_cmd(c.LSTICK_CENTER) ; time.sleep(0.1)  
    c.send_cmd(c.LSTICK_R) ; time.sleep(0.7) ;  c.send_cmd(c.LSTICK_CENTER) ; time.sleep(0.1)  
    c.send_cmd(c.BTN_A) ; time.sleep(0.1) ;  c.send_cmd() ; time.sleep(0.1)  
    return True

def getEggFromBreader(c):
    print("getEggFromBreader")
    c.send_cmd(c.BTN_A) ; time.sleep(0.1) ;  c.send_cmd();  time.sleep(3)  
    c.send_cmd(c.BTN_A) ; time.sleep(0.1) ;  c.send_cmd();  time.sleep(5)  
    c.send_cmd(c.BTN_A) ; time.sleep(0.1) ;  c.send_cmd();  time.sleep(4)
    # select pokemon to swap prompt
    time.sleep(1.5)
    c.send_cmd(c.BTN_A) ; time.sleep(0.1) ;  c.send_cmd();  time.sleep(1)  
    c.send_cmd(c.BTN_A) ; time.sleep(0.1) ;  c.send_cmd();  time.sleep(0.4)    
    # select pokemon to swap box screen
    time.sleep(1.5)
    c.send_cmd(c.DPAD_D) ; time.sleep(0.2) ;  c.send_cmd();  time.sleep(1)  
    c.send_cmd(c.BTN_A) ; time.sleep(0.1) ;  c.send_cmd();  time.sleep(1)  
    # egg will be added to party prompt
    time.sleep(2)
    c.send_cmd(c.BTN_A) ; time.sleep(0.1) ;  c.send_cmd();  time.sleep(0.4)
    # raise it well prompt
    time.sleep(2)
    c.send_cmd(c.BTN_A) ; time.sleep(0.1) ;  c.send_cmd();  time.sleep(0.3)
    return True

def circles(c, num):
    animation_time = 0.2
    for i in range(num):
        print ("Circle #{}".format(i))
        c.send_cmd(c.LSTICK_R) ; time.sleep(0.2 + animation_time) ;   time.sleep(0.1)  ;       c.send_cmd(c.LSTICK_CENTER) ; time.sleep(0.1)  
        c.send_cmd(c.LSTICK_D) ; time.sleep(0 + animation_time) ;  time.sleep(0.1)  ;       c.send_cmd(c.LSTICK_CENTER) ; time.sleep(0.1)  
        c.send_cmd(c.LSTICK_L) ; time.sleep(0.2 + animation_time); time.sleep(0.1)  ;       c.send_cmd(c.LSTICK_CENTER) ; time.sleep(0.1)  
        c.send_cmd(c.LSTICK_U) ; time.sleep(0 + animation_time) ;   time.sleep(0.1)  ;       c.send_cmd(c.LSTICK_CENTER) ; time.sleep(0.1)   
        if stop_threads: 
            break       
    return True

def mashA (c, num):
    print ("mashing A")
    for i in range(num):
        c.send_cmd(c.BTN_A) ; time.sleep(0.1) ;  c.send_cmd();  time.sleep(0.5)
        if stop_threads: 
            break       
    return True    
        

ps3_buttons = {
    "Y": 15,
    "X": 12,
    "B": 14,
    "A": 13,  
    "DIR_U": 4,
    "DIR_R": 5,
    "DIR_D": 6,
    "DIR_L": 7,  
    "R1" : 11,
    "L1" : 10,
    "R2" : 9,
    "L2" : 8,
    "R3" : 2,
    "L3" : 1,
    "+" : 3,
    "-" : 0,
    "PS" : 16
}

def joystickfiltering(value):
    #deadzone
    if abs(value) <= .15:
        value = 0
    
    if value >= .95:
        value = 1

    if value <= -0.95:
        value = -1


    return value

def getButtonPayload (button_values):
    decoded_buttons = 0
    # get buttons held down
    for index in range(len(button_values)):
        if (button_values[index] == 1):
            decoded_buttons = mapSwitchToPS3(c, index) + decoded_buttons
    
    return decoded_buttons

# event.button
def mapSwitchToPS3 (client2, input_num):
    if input_num == ps3_buttons['DIR_U']:
        dpadDecrypt = client2.DPAD_U
    elif input_num == ps3_buttons['DIR_R']:
        dpadDecrypt = client2.DPAD_R
    elif input_num == ps3_buttons['DIR_D']:
        dpadDecrypt = client2.DPAD_D
    elif input_num == ps3_buttons['DIR_L']:
        dpadDecrypt = client2.DPAD_L
    elif input_num == ps3_buttons['Y']:
        dpadDecrypt = client2.BTN_Y     
    elif input_num == ps3_buttons['X']:
        dpadDecrypt = client2.BTN_X     
    elif input_num == ps3_buttons['B']:
        dpadDecrypt = client2.BTN_B     
    elif input_num == ps3_buttons['A']:
        dpadDecrypt = client2.BTN_A
    elif input_num == ps3_buttons['R1']:
        dpadDecrypt = client2.BTN_R     
    elif input_num == ps3_buttons['L1']:
        dpadDecrypt = client2.BTN_L      
    elif input_num == ps3_buttons['R2']:
        dpadDecrypt = client2.BTN_ZR     
    elif input_num == ps3_buttons['L2']:
        dpadDecrypt = client2.BTN_ZL     
    elif input_num == ps3_buttons['R3']:
        dpadDecrypt = client2.BTN_RCLICK     
    elif input_num == ps3_buttons['L3']:
        dpadDecrypt = client2.BTN_LCLICK   
    elif input_num == ps3_buttons['R3']:
        dpadDecrypt = client2.BTN_RCLICK     
    elif input_num == ps3_buttons['L3']:
        dpadDecrypt = client2.BTN_LCLICK   
    elif input_num == ps3_buttons['+']:
        dpadDecrypt = client2.BTN_PLUS     
    elif input_num == ps3_buttons['-']:
        dpadDecrypt = client2.BTN_MINUS   
    elif input_num == ps3_buttons['PS']:
        dpadDecrypt = client2.BTN_HOME                   
    else:
        dpadDecrypt = client2.A_DPAD_CENTER    
    return dpadDecrypt


pygame.init()
j = pygame.joystick.Joystick(0)
j.init()

if not c.sync():
    print('Could not sync!')


t2 = threading.Thread(target=macro2_thread, args=(c,)) 

try:
    while True:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.JOYAXISMOTION:
                filtered_value = joystickfiltering(event.value)
                #filtered_value = event.value
                diff = abs(axis_history[event.axis] - filtered_value)
                if (diff > .05):
                    if (event.axis == 0):
                        x = filtered_value * axis_invert[0]
                        y = axis_history[1]
                    elif (event.axis == 1):
                        y = filtered_value * axis_invert[1]
                        x = axis_history[0]  
                    elif (event.axis == 2):
                        x = filtered_value * axis_invert[2]
                        y = axis_history[3]  
                    elif (event.axis == 3):
                        y = filtered_value * axis_invert[3]
                        x = axis_history[2]                                                                        
                    angle = math.atan2(y, x)
                    angle = math.degrees(angle)
                    angle = round(angle)
                    if (angle < 0):
                        angle = 180 + (180 + angle)
                    print ("{}, {} angle: {}".format(x, y, angle))
                    if (event.axis == 0 or event.axis == 1):
                        cmd = c.lstick_angle(angle, 0xFF) + c.rstick_angle(0, 0x00)
                        if x == 0 and y == 0:
                            cmd = c.lstick_angle(angle, 0x00) + c.rstick_angle(0, 0x00)
                    if (event.axis == 2 or event.axis == 3):
                        cmd = c.lstick_angle(0, 0x00) + c.rstick_angle(angle, 0xFF)
                        if x == 0 and y == 0:
                            cmd = c.lstick_angle(0, 0x00) + c.rstick_angle(angle, 0x00)                    
                    c.send_cmd(cmd)
                    c.p_wait(0.001)
                    print(event.dict, event.joy, event.axis, event.value)
                    
                axis_history[event.axis] = filtered_value * axis_invert[event.axis]
            elif event.type == pygame.JOYBALLMOTION:
                print(event.dict, event.joy, event.ball, event.rel)
            elif event.type == pygame.JOYBUTTONDOWN:
                print(event.dict, event.joy, event.button, 'pressed')
                button_values[event.button] = 1
                switch_button = getButtonPayload(button_values)
                if (button_values[ps3_buttons['L1']] and button_values[ps3_buttons['DIR_U']]):
                    print ("Run a macro")
                    stop_threads = False
                    t1 = threading.Thread(target=macro1_thread, args=(c,)) 
                    t1.start()
                elif (button_values[ps3_buttons['L1']] and button_values[ps3_buttons['DIR_L']]):
                    print ("Run a macro")
                    stop_threads = False
                    t2.start()                    
                elif (button_values[ps3_buttons['L1']] and button_values[ps3_buttons['DIR_D']]):
                    print ("Stop a macro")
                    stop_threads = True
                    t1.join() 
                else:
                    c.send_cmd(switch_button)
                    c.p_wait(0.001)
            elif event.type == pygame.JOYBUTTONUP:
                print(event.dict, event.joy, event.button, 'released')
                button_values[event.button] = 0
                switch_button = getButtonPayload(button_values)
                c.send_cmd(switch_button) 
                c.p_wait(0.001)
            elif event.type == pygame.JOYHATMOTION:
                print(event.dict, event.joy, event.hat, event.value)
        time.sleep(0.05)

except KeyboardInterrupt:
    print("EXITING NOW")
    j.quit()