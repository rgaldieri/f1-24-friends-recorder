import sys

from packet_management import *
import json
import time
from dictionnaries import *
from parser2024 import Listener

with open("settings.txt", "r") as f:
    dictionnary_settings = json.load(f)

if len(sys.argv)==2:
    dictionnary_settings["port"] = int(sys.argv[1])

running = True

PORT = [int(dictionnary_settings["port"])]
listener = Listener(port=PORT[0],
                    redirect=dictionnary_settings["redirect_active"],
                    adress=dictionnary_settings["ip_adress"],
                    redirect_port=int(dictionnary_settings["redirect_port"]))

packet_received = [0]*15
last_update = time.time()

function_hashmap = { #PacketId : (fonction, arguments)
    0: (nothing, ()), # Motion
    1: (n_update_session, ()), # Session
    2: (nothing, ()), # Lap Data
    3: (nothing, ()), # Event
    4: (n_update_participants, ()), #  Participants
    5: (nothing, ()), # Setups
    6: (nothing, ()), # Telemetry
    7: (nothing, ()), # Car Status
    8: (nothing, ()), # Final Classification 
    9: (nothing, ()), # Lobby Info
    10: (nothing, ()), # Car Damage
    11: (nothing, ()), # Session History
    12: (nothing, ()), # Tyre Set
    13: (nothing, ()), # Motion Ex
    14: (n_time_trial, ()) # Time Trial Data
}

print("Server listening")
while running:
    a = listener.get()
    if a is not None:
        header, packet = a
        packet_received[header.m_packet_id]+=1
        func, args = function_hashmap[header.m_packet_id]
        func(packet, header, *args)
    if time.time() > last_update+1:
        last_update = time.time()
        session.packet_received = packet_received[:]
        packet_received = [0]*15
    
listener.socket.close()
quit()
