#!/usr/bin/python

import smbus
import time

bus = smbus.SMBus(1)

INPUT = 0x26
OUTPUT = 0x27

DIRA = 0x00
DIRB = 0x01
GPIOA = 0x12
GPIOB = 0x13

switches = {
    GPIOA: {
        0x02: { #wejscie 
            'port': GPIOA,
            'pin': 64
        },
        0x03: { #wejscie 2 
            'port': GPIOA,
            'pin': 64
        },
        0x01: { #lazienka 1
            'port': GPIOA,
            'pin': 16
        },
        0x00: { #lazienka 2 
            'port': GPIOA,
            'pin': 0x01
        },
        0x05: { #lazienka lustro 
            'port': GPIOA,
            'pin': 0x01
        },
        0x07: { #salon
            'port': GPIOA,
            'pin': 32
        },        
        0x06: { #sypialnia
            'port': GPIOA,
            'pin': 2
        }
    },
    GPIOB: {
        0x01: { #kuchnia 1 
            'port': GPIOA,
            'pin': 8
        }
    }
}

states = {}
INPORTS = {}

#init input
bus.write_byte_data(INPUT, DIRA, 0xFF)
bus.write_byte_data(INPUT, DIRB, 0xFF)

# init output
bus.write_byte_data(OUTPUT, DIRA, 0)
bus.write_byte_data(OUTPUT, DIRB, 0)



def read_action(gpio):
    change = False        
    read = bus.read_byte_data(INPUT, gpio)
    diff = INPORTS[gpio] ^ read
    for i in range(0, 8):
        if diff & (1 << i):
            if i in switches[gpio]:
                result = switches[gpio][i]
                print gpio, i, result
                states[result['port']] ^= result['pin']
                change = True
            else:
                print "! unknown key"
    INPORTS[gpio] = read
    return change

states[GPIOA] = bus.read_byte_data(OUTPUT, GPIOA)
states[GPIOB] = bus.read_byte_data(OUTPUT, GPIOB)
INPORTS[GPIOA] = bus.read_byte_data(INPUT, GPIOA)
INPORTS[GPIOB] = bus.read_byte_data(INPUT, GPIOB)

while True:

    if read_action(GPIOA) or read_action(GPIOB):
        bus.write_byte_data(OUTPUT, GPIOA, states[GPIOA])
        bus.write_byte_data(OUTPUT, GPIOB, states[GPIOB])

    time.sleep(0.2)