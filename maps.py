#!/usr/bin/python

INPUT = 0x26
OUTPUT = 0x27

DIRA = 0x00
DIRB = 0x01
GPIOA = 0x12
GPIOB = 0x13

switches = {
    GPIOA: {
        0x00: { #lazienka 2 
            'port': GPIOB,
            'pin': 5
        },
        0x01: { #lazienka 1
            'port': GPIOA,
            'pin': 4
        },
        0x02: { #wejscie 
            'port': GPIOA,
            'pin': 6
        },
        0x03: { #wejscie 2 
            'port': GPIOA,
            'pin': 6
        },  
        0x04: { #blat kuchnia 1
            'port': GPIOA,
            'pin': 3
        },       
        0x05: { #lazienka lustro 
            'port': GPIOB,
            'pin': 5
        },
        0x07: { #salon
            'port': GPIOA,
            'pin': 5
        },        
        0x06: { #sypialnia
            'port': GPIOA,
            'pin': 1
        }
    },
    GPIOB: {
        0x00: { #kuchnia 1 
            'port': GPIOA,
            'pin': 3
        },
        0x01: { #kuchnia 2
            'port': GPIOB,
            'pin': 4
        },
        0x02: { #blat w kuchni 2
            'port': GPIOB,
            'pin': 4
        }
    }
}

output_states = {}
input_states = {}
