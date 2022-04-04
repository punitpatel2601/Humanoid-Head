#!/usr/bin/env python3

# EMOTION_NAME = [RIGHT EAR SERVO ANGLE, LEFT EAR SERVO ANGLE]
Idle = [90, 90]
Danger = [180, 180]
Caution = [0, 0]


# Flags to priortize emotions
gas_flag = False
manual_flag = False

gas_emot = Idle
man_emot = Idle
default_emot = Idle


# Sets overall emotion - prioritizing gas, followed by manual
def set_emotion():
    if gas_flag == True:
        return gas_emot
    elif manual_flag == True:
        return man_emot
    else:
        return default_emot


# Emotion set by operator
def man_set_emotion(id):
    if id == 1:
        manual_flag = True
        print("Man - Danger\n")
        man_emot = Danger
    elif id == 2:
        manual_flag = True
        print("Man - Caution\n")
        man_emot = Caution
    else:
        manual_flag = False
        
# Emotions set by gas monitoring node
def gas_selected_emotion(id):  
    if id == 1:
        gas_flag = True
        print("Gas - Danger\n")
        gas_emot = Danger
    elif id == 2:
        gas_flag = True
        print("Gas - Caution\n")
        gas_emot = Caution
    else:
        gas_flag = False
        print("Idle\n")
