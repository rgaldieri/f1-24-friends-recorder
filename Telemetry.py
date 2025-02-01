from ttkbootstrap import Window, Notebook, Frame, Canvas, Menu, Label
import sys

screen = Window(themename="darkly")

from packet_management import *
import json
import time
from dictionnaries import *
from parser2024 import Listener
from Custom_Frame import Players_Frame, Packet_Reception_Frame, Weather_Forecast_Frame

def init_window():
    global map_canvas
    screen.columnconfigure(0, weight=1)
    screen.rowconfigure(0, pad=75)
    screen.rowconfigure(1, weight=1)

    screen.title("Time Trial Data Sender")

    top_frame.grid(row=0, column=0, columnspan=3, sticky="nsew")
    main_frame.grid(row=1, column=0, sticky="nsew")

    notebook = Notebook(main_frame)
    notebook.pack(expand=True, fill="both")

    LISTE_FRAMES.append(Players_Frame(notebook, "Main Menu", 0))
    LISTE_FRAMES.append(Players_Frame(notebook, "Damage", 1))
    LISTE_FRAMES.append(Players_Frame(notebook, "Temperatures", 2))
    LISTE_FRAMES.append(Players_Frame(notebook, "Laps", 3))
    LISTE_FRAMES.append(Players_Frame(notebook, "ERS & Fuel", 4))

    map = Frame(notebook)
    LISTE_FRAMES.append(map)
    map.pack(expand=True, fill="both")
    map_canvas = Canvas(map)
    map_canvas.pack(expand=True, fill='both')

    LISTE_FRAMES.append(Packet_Reception_Frame(notebook, "Packet Reception", 6))

    for i in range(len(LISTE_FRAMES)):
        if i != 5:
            notebook.add(LISTE_FRAMES[i], text=LISTE_FRAMES[i].name)
        else:
            notebook.add(LISTE_FRAMES[5], text="Map")

    top_label1.place(relx=0.0, rely=0.5, anchor='w')
    top_label2.place(relx=1, rely=0.5, anchor='e', relheight=1)
    top_frame.columnconfigure(0, weight=3)

    screen.geometry("1480x800")
    screen.protocol("WM_DELETE_WINDOW", close_window)

def close_window():
    global running
    running = False
'''
indice 7,27,28,29
21 = multiple warnings
'''

packet_received = [0]*15
last_update = time.time()

with open("settings.txt", "r") as f:
    dictionnary_settings = json.load(f)

if len(sys.argv)==2:
    dictionnary_settings["port"] = int(sys.argv[1])

top_frame = Frame(screen)
main_frame = Frame(screen)

top_label1 = Label(top_frame, text="Course ", font=("Arial", 24))
top_label2 = Label(top_frame, text="", font=("Arial", 24), width=10)

init_window()
init_20_players()

running = True
PORT = [int(dictionnary_settings["port"])]
listener = Listener(port=PORT[0],
                    redirect=dictionnary_settings["redirect_active"],
                    adress=dictionnary_settings["ip_adress"],
                    redirect_port=int(dictionnary_settings["redirect_port"]))

function_hashmap = { #PacketId : (fonction, arguments)
    # 0: (update_motion, (map_canvas, None)), # Motion
    # 1: (update_session, (top_label1, top_label2, screen, map_canvas)), # Session
    # 2: (update_lap_data, ()), # Lap Data
    # 4: (update_participants, ()), #  Participants
    # 5: (update_car_setups, ()), # Setups
    # 6: (update_car_telemetry, ()), # Telemetry
    # 7: (update_car_status, ()), # Car Status
    # 10: (update_car_damage, ()), # Car Damage
    0: (nothing, ()), # Motion
    1: (nothing, ()), # Session
    2: (n_update_lap_data, ()), # Lap Data
    3: (nothing, ()), # Event
    4: (nothing, ()), #  Participants
    5: (nothing, ()), # Setups
    6: (nothing, ()), # Telemetry
    7: (nothing, ()), # Car Status
    8: (nothing, ()), # Final Classification 
    9: (nothing, ()), # Lobby Info
    10: (nothing, ()), # Car Damage
    11: (nothing, ()), # Session History
    12: (nothing, ()), # Tyre Set
    13: (nothing, ()), # Motion Ex
    14: (time_trial, ()) # Time Trial Data
}

while running:
    a = listener.get()
    if a is not None:
        header, packet = a
        packet_received[header.m_packet_id]+=1
        func, args = function_hashmap[header.m_packet_id]
        func(packet, header, *args)
    if time.time() > last_update+1:
        last_update = time.time()
        LISTE_FRAMES[len(LISTE_FRAMES)-1].update(packet_received) #Packet Received tab
        session.packet_received = packet_received[:]
        packet_received = [0]*15
    screen.update()
    screen.update_idletasks()
    
listener.socket.close()
quit()
