#!/usr/bin/python
import smbus
import paho.mqtt.client as mqtt
import time
from maps import *
from threading import Thread
import sys

bus = smbus.SMBus(1)

#init input
bus.write_byte_data(INPUT, DIRA, 0xFF)
bus.write_byte_data(INPUT, DIRB, 0xFF)

# init output
bus.write_byte_data(OUTPUT, DIRA, 0)
bus.write_byte_data(OUTPUT, DIRB, 0)

def read_action(gpio):
    read = bus.read_byte_data(INPUT, gpio)
    diff = input_states[gpio] ^ read
    out = []
    for i in range(0, 8):
        if diff & (1 << i):
            if i in switches[gpio]:
                result = switches[gpio][i]
                print gpio, i, "mapped output =>", result
                output_states[result['port']] ^= (1 << result['pin'])
                out.append(result)
            else:
                print "! unknown key", gpio, i
    input_states[gpio] = read
    return out

#initial state
output_states[GPIOA] = bus.read_byte_data(OUTPUT, GPIOA)
output_states[GPIOB] = bus.read_byte_data(OUTPUT, GPIOB)
input_states[GPIOA] = bus.read_byte_data(INPUT, GPIOA)
input_states[GPIOB] = bus.read_byte_data(INPUT, GPIOB)
input_states[SPECIAL_FUNCTIONS] = 0
output_states[SPECIAL_FUNCTIONS] = 0

def on_connect(client, userdata, flags, rc):
    print("Connected to mqtt with result code "+str(rc))
    client.subscribe("home/lights/+/+/switch")

def on_message(client, userdata, msg):
    exploded = msg.topic.split('/')
    if len(exploded) > 4:
        port = int(exploded[2])
        pin = int(exploded[3])

        if port in output_states:
            if msg.payload == 'ON':
                output_states[port] |= (1 << pin)
                bus.write_byte_data(OUTPUT, port, output_states[port])
            elif msg.payload == 'OFF':
                output_states[port] &= ~(1 << pin)
                bus.write_byte_data(OUTPUT, port, output_states[port])

            client.publish("home/lights/{}/{}/state".format(port, pin), msg.payload, retain=True)


    print(msg.topic+" "+str(msg.payload))

client = mqtt.Client("smart-home-python-script")
client.on_connect = on_connect
client.on_message = on_message
client.username_pw_set(sys.argv[2], sys.argv[3])
client.connect(sys.argv[1], 19470)

thread = Thread(target = client.loop_forever)
thread.daemon = True
thread.start()

while True:
    diffa = read_action(GPIOA)
    diffb = read_action(GPIOB)

    for ind in diffa + diffb:
        client.publish("home/lights/{}/{}/state".format(ind['port'], ind['pin']), "ON" if output_states[ind['port']] & (1 << ind['pin']) else "OFF", retain=True)

    if diffa or diffb:
        bus.write_byte_data(OUTPUT, GPIOA, output_states[GPIOA])
        bus.write_byte_data(OUTPUT, GPIOB, output_states[GPIOB])
    time.sleep(0.05)
