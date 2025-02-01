from Session import Session
from DataMemory import DataMemory
from Player import Player
from dictionnaries import *
import json
from parser2023 import Listener
import math
import time
from ttkbootstrap import Toplevel, LEFT, Entry, IntVar, Label
from tkinter import Message, Checkbutton, Button
from Custom_Frame import Custom_Frame
import traceback

BestTimeInMS = -1
LOCAL_PLAYER_ID = -1
session: Session = Session()
TT_data : DataMemory = DataMemory()

PLAYERS_LIST: list[Player] = []
created_map = False
WIDTH_POINTS = 6
LISTE_FRAMES = []


def time_trial(packet, header):
    global BestTimeInMS
    if(BestTimeInMS == -1):
        print("Time Initialization")
        #Initializing data
        LOCAL_PLAYER_ID = header.m_player_car_index
        session_best = packet.m_playerSessionBestDataSet # Player session best data set
        if(packet.m_personalBestDataSet.m_lap_time_in_ms > 0):
            BestTimeInMS = packet.m_personalBestDataSet.m_lap_time_in_ms
            print("Best time is " + str(BestTimeInMS))
        else:
            print("No Best Time Recorded")
            BestTimeInMS = 999999999
    if(packet.m_personalBestDataSet.m_lap_time_in_ms < BestTimeInMS and packet.m_personalBestDataSet.m_lap_time_in_ms > 0):
        BestTimeInMS = packet.m_playerSessionBestDataSet.m_lap_time_in_ms
        print("New Best:" + str(BestTimeInMS))

def update_motion(packet, map_canvas, *args):  # Packet 0
    for i in range(session.nb_players):
        if PLAYERS_LIST[i].worldPositionX != 0:
            PLAYERS_LIST[i].Xmove = packet.m_car_motion_data[i].m_world_position_x - PLAYERS_LIST[i].worldPositionX
            PLAYERS_LIST[i].Zmove = packet.m_car_motion_data[i].m_world_position_z - PLAYERS_LIST[i].worldPositionZ
        PLAYERS_LIST[i].worldPositionX = packet.m_car_motion_data[i].m_world_position_x
        PLAYERS_LIST[i].worldPositionZ = packet.m_car_motion_data[i].m_world_position_z
    try:
        update_map(map_canvas)
    except Exception as e:
        try:
            traceback.print_exc()
            create_map(map_canvas)
        except Exception as e :
            pass

def update_session(packet, top_frame1, top_frame2, screen, map_canvas):  # Packet 1
    global created_map
    session.trackTemperature = packet.m_weather_forecast_samples[0].m_track_temperature
    session.airTemperature = packet.m_weather_forecast_samples[0].m_air_temperature
    session.nbLaps = packet.m_total_laps
    session.time_left = packet.m_session_time_left
    if session.track != packet.m_track_id or session.Seance != packet.m_session_type: # Track or session has changed
        session.track = packet.m_track_id
        delete_map(map_canvas)
    session.Seance = packet.m_session_type
    session.marshalZones = packet.m_marshal_zones  # Array[21]
    session.marshalZones[0].m_zone_start = session.marshalZones[0].m_zone_start - 1
    session.num_marshal_zones = packet.m_num_marshal_zones
    session.safetyCarStatus = packet.m_safety_car_status
    session.trackLength = packet.m_track_length
    session.clear_slot()
    if packet.m_num_weather_forecast_samples != session.nb_weatherForecastSamples:
        session.nb_weatherForecastSamples = packet.m_num_weather_forecast_samples
        #Reconstruire le tableau 
    for i in range(session.nb_weatherForecastSamples):
        slot = packet.m_weather_forecast_samples[i]
        session.add_slot(slot)
    update_title(top_frame1, top_frame2, screen)
    update_frame6()

def update_lap_data(packet, header):  # Packet 2
    mega_array = packet.m_lap_data
    for index in range(22):
        element = mega_array[index]
        player = PLAYERS_LIST[index]
        player.position = element.m_car_position
        player.lastLapTime = round(element.m_last_lap_time_in_ms, 3)
        player.pit = element.m_pit_status
        player.driverStatus = element.m_driver_status
        player.penalties = element.m_penalties
        player.warnings = element.m_corner_cutting_warnings
        player.speed_trap = round(element.m_speedTrapFastestSpeed, 2)
        player.currentLapTime = element.m_current_lap_time_in_ms
        player.delta_to_leader=element.m_deltaToCarInFrontMSPart
        player.currentLapInvalid = element.m_current_lap_invalid

        if element.m_sector1_time_in_ms == 0 and player.currentSectors[0] != 0:  # Starting a new lap
            player.lastLapSectors = player.currentSectors[:]
            player.lastLapSectors[2] = player.lastLapTime / 1_000 - player.lastLapSectors[0] - player.lastLapSectors[1]

        player.currentSectors = [element.m_sector1_time_in_ms / 1000, element.m_sector2_time_in_ms / 1000, 0]
        if player.bestLapTime > element.m_last_lap_time_in_ms != 0 or player.bestLapTime == 0:
            player.bestLapTime = element.m_last_lap_time_in_ms
            player.bestLapSectors = player.lastLapSectors[:]
        if player.bestLapTime < session.bestLapTime and element.m_last_lap_time_in_ms != 0 or player.bestLapTime == 0:
            session.bestLapTime = player.bestLapTime
            session.idxBestLapTime = index
        if element.m_car_position == 1:
            session.currentLap = mega_array[index].m_current_lap_num
            session.tour_precedent = session.currentLap - 1

def n_update_lap_data(packet, header):
    # last_lap_time = packet.m_lap_data[header.m_player_car_index]
    # if last_lap_time < LastLapTimeInMS:
    #     LastLapTimeInMS = last_lap_time
    #     print("Time Updated")
    pass
    # LOCAL_PLAYER_ID = header.m_player_car_index
    # lapData = packet.m_lap_data[LOCAL_PLAYER_ID]


    # session_best = packet.m_playerSessionBestDataSet # Player session best data set
    # alltime_best = packet.m_personalBestDataSet
    # if(not tt_data.initialized):
    #     TT_data.initialize(alltime_best)
    # if packet.m_lap_data[LOCAL_PLAYER_ID].m_sector1_time_in_ms == 0:
    #     print("New Lap")
    # mega_array = packet.m_lap_data
    # for index in range(22):
    #     element = mega_array[index]
    #     player = PLAYERS_LIST[index]
    #     player.position = element.m_car_position
    #     player.lastLapTime = round(element.m_last_lap_time_in_ms, 3)
    #     player.pit = element.m_pit_status
    #     player.driverStatus = element.m_driver_status
    #     player.penalties = element.m_penalties
    #     player.warnings = element.m_corner_cutting_warnings
    #     player.speed_trap = round(element.m_speedTrapFastestSpeed, 2)
    #     player.currentLapTime = element.m_current_lap_time_in_ms
    #     player.delta_to_leader=element.m_deltaToCarInFrontMSPart
    #     player.currentLapInvalid = element.m_current_lap_invalid

    #     if element.m_sector1_time_in_ms == 0 and player.currentSectors[0] != 0:  # New Lap?
    #         player.lastLapSectors = player.currentSectors[:]
    #         player.lastLapSectors[2] = player.lastLapTime / 1_000 - player.lastLapSectors[0] - player.lastLapSectors[1]

    #     player.currentSectors = [element.m_sector1_time_in_ms / 1000, element.m_sector2_time_in_ms / 1000, 0]
    #     if player.bestLapTime > element.m_last_lap_time_in_ms != 0 or player.bestLapTime == 0:
    #         player.bestLapTime = element.m_last_lap_time_in_ms
    #         player.bestLapSectors = player.lastLapSectors[:]
    #     if player.bestLapTime < session.bestLapTime and element.m_last_lap_time_in_ms != 0 or player.bestLapTime == 0:
    #         session.bestLapTime = player.bestLapTime
    #         session.idxBestLapTime = index
    #     if element.m_car_position == 1:
    #         session.currentLap = mega_array[index].m_current_lap_num
    #         session.tour_precedent = session.currentLap - 1

def events(packet, header):  # Packet 3
    if packet.m_event_string_code[3] == 71 and packet.m_event_details.m_start_lights.m_num_lights >= 2: # Starts lights : STLG
        session.formationLapDone = True
        print(f"{packet.m_event_details.m_start_lights.m_num_lights} red lights ")
    elif packet.m_event_string_code[0] == 76 and session.formationLapDone: #Lights out : LGOT
        print("Lights out !")
        session.formationLapDone = False
        session.startTime = time.time()
        for player in PLAYERS_LIST:
            player.S200_reached = False
            player.warnings = 0
            player.lastLapSectors = [0] * 3
            player.bestLapSectors = [0] * 3
            player.lastLapTime: float = 0
            player.currentSectors = [0] * 3
            player.bestLapTime = 0
    elif packet.m_event_string_code[2] == 82:
        PLAYERS_LIST[packet.m_event_details.m_vehicle_idx].hasRetired = True

def update_participants(packet, header):  # Packet 4
    for index in range(22):
        element = packet.m_participants[index]
        player = PLAYERS_LIST[index]
        player.numero = element.m_race_number
        player.teamId = element.m_team_id
        player.aiControlled = element.m_ai_controlled
        player.yourTelemetry = element.m_your_telemetry
        try:
            player.name = element.m_name.decode("utf-8")
        except:
            player.name = element.m_name
        session.nb_players = packet.m_num_active_cars
        if player.name in ['Player', 'Joueur']:
            player.name = teams_name_dictionary[player.teamId] + "#" + str(player.numero)
    update_frame(LISTE_FRAMES, PLAYERS_LIST, session)

def update_car_setups(packet, header): # Packet 5
    array = packet.m_car_setups
    for index in range(22):
        PLAYERS_LIST[index].setup_array = array[index]

def update_car_telemetry(packet, header):  # Packet 6
    for index in range(22):
        element = packet.m_car_telemetry_data[index]
        player = PLAYERS_LIST[index]
        player.drs = element.m_drs
        player.tyres_temp_inner = element.m_tyres_inner_temperature
        player.tyres_temp_surface = element.m_tyres_surface_temperature
        player.speed = element.m_speed
        if player.speed >= 200 and not player.S200_reached:
            print(f"{player.position} {player.name}  = {time.time() - session.startTime}")
            player.S200_reached = True
    update_frame(LISTE_FRAMES, PLAYERS_LIST, session)

def update_car_status(packet, header):  # Packet 7
    for index in range(22):
        element = packet.m_car_status_data[index]
        player = PLAYERS_LIST[index]
        player.fuelMix = element.m_fuel_mix
        player.fuelRemainingLaps = element.m_fuel_remaining_laps
        player.tyresAgeLaps = element.m_tyres_age_laps
        if player.tyres != element.m_visual_tyre_compound:
            player.tyres = element.m_visual_tyre_compound
        player.ERS_mode = element.m_ers_deploy_mode
        player.ERS_pourcentage = round(element.m_ers_store_energy / 40_000)
    update_frame(LISTE_FRAMES, PLAYERS_LIST, session)

def update_car_damage(packet, header):  # Packet 10
    for index in range(22):
        element = packet.m_car_damage_data[index]
        player = PLAYERS_LIST[index]
        player.tyre_wear = '[' + ', '.join('%.2f'%truc for truc in element.m_tyres_wear) + ']'
        player.FrontLeftWingDamage = element.m_front_left_wing_damage
        player.FrontRightWingDamage = element.m_front_right_wing_damage
        player.rearWingDamage = element.m_rear_wing_damage
        player.floorDamage = element.m_floor_damage
        player.diffuserDamage = element.m_diffuser_damage
        player.sidepodDamage = element.m_sidepod_damage
    update_frame(LISTE_FRAMES, PLAYERS_LIST, session)

def nothing(packet, header):# Packet 8, 9, 11, 12, 13
    pass

def create_map(map_canvas):
    cmi = 1
    L0, L1 = [], []
    L = []
    name, d, x_const, z_const = track_dictionary[session.track]
    with open(f"tracks/{name}_2020_racingline.txt", "r") as file:
        for index, line in enumerate(file):
            if index not in [0, 1]:
                dist, z, x, y, _, _ = line.strip().split(",")
                if cmi == 1:
                    L0.append((float(z) / d + x_const, float(x) / d + z_const))
                elif cmi == session.num_marshal_zones:
                    L1.append((float(z) / d + x_const, float(x) / d + z_const))
                else:
                    L.append((float(z) / d + x_const, float(x) / d + z_const))
                if (float(dist) / session.trackLength) > session.marshalZones[cmi].m_zone_start and cmi!=session.num_marshal_zones:
                    if cmi != 1:
                        session.segments.append(map_canvas.create_line(L, width=3))
                        L = []
                    cmi +=1
    session.segments.insert(0, map_canvas.create_line(L1+L0, width=3))
    for i in range(20):
        player = PLAYERS_LIST[i]
        if session.Seance == 18 and i!=0:
            player.oval = map_canvas.create_oval(-1000 / d + x_const - WIDTH_POINTS,
                                                -1000 / d + z_const - WIDTH_POINTS,
                                                -1000 / d + x_const + WIDTH_POINTS,
                                                -1000 / d + z_const + WIDTH_POINTS, outline="")
        else:
            player.oval = map_canvas.create_oval(player.worldPositionX / d + x_const - WIDTH_POINTS,
                                                player.worldPositionZ / d + z_const - WIDTH_POINTS,
                                                player.worldPositionX / d + x_const + WIDTH_POINTS,
                                                player.worldPositionZ / d + z_const + WIDTH_POINTS, outline="")
            
            player.etiquette = map_canvas.create_text(player.worldPositionX / d + x_const + 25,
                                                    player.worldPositionZ / d + z_const - 25,
                                                    text=player.name, font=("Cousine", 13))
            map_canvas.moveto(player.oval, player.worldPositionX / d + x_const - WIDTH_POINTS,
                                player.worldPositionZ / d + z_const - WIDTH_POINTS)

def delete_map(map_canvas):
    for element in session.segments:
        map_canvas.delete(element)
    session.segments = []
    for player in PLAYERS_LIST:
        map_canvas.delete(player.oval)
        map_canvas.delete(player.etiquette)
        player.oval = None

def update_map(map_canvas):
    _, d, x, z = track_dictionary[session.track]
    for player in PLAYERS_LIST:
        if player.position != 0:
            map_canvas.move(player.oval, player.Xmove / d, player.Zmove / d)
            map_canvas.itemconfig(player.oval, fill=teams_color_dictionary[player.teamId])
            map_canvas.move(player.etiquette, player.Xmove / d, player.Zmove / d)
            map_canvas.itemconfig(player.etiquette, fill=teams_color_dictionary[player.teamId], text=player.name)
    for i in range(len(session.segments)):
        map_canvas.itemconfig(session.segments[i], fill=color_flag_dict[session.marshalZones[i].m_zone_flag])
    session.anyYellow = any(item.m_zone_flag==3 for item in session.marshalZones)
        
def init_20_players():
    for _ in range(22):
        PLAYERS_LIST.append(Player())

def UDP_Redirect(dictionnary_settings, listener, PORT):
    win = Toplevel()
    win.grab_set()
    win.wm_title("UDP Redirect")
    var1 = IntVar(value=dictionnary_settings["redirect_active"])
    checkbutton = Checkbutton(win, text="UDP Redirect", variable=var1, onvalue=1, offvalue=0, font=("Arial", 16))
    checkbutton.grid(row=0, column=0, sticky="W", padx=30, pady=10)
    Label(win, text="IP Address", font=("Arial", 16), justify=LEFT).grid(row=1, column=0, pady=10)
    e1 = Entry(win, font=("Arial", 16))
    e1.insert(0, dictionnary_settings["ip_adress"])
    e1.grid(row=2, column=0)
    Label(win, text="Port", font=("Arial", 16)).grid(row=3, column=0, pady=(10, 5))
    e2 = Entry(win, font=("Arial", 16))
    e2.insert(0, dictionnary_settings["redirect_port"])
    e2.grid(row=4, column=0, padx=30)

    def button():
        redirect_port = e2.get()
        if not redirect_port.isdigit() or not 1000 <= int(redirect_port) <= 65536:
            Message(win, text="The PORT must be an integer between 1000 and 65536", fg="red", font=("Arial", 16)).grid(
                row=6, column=0)
        elif not valid_ip_address(e1.get()):
            Label(win, text="IP Address incorrect", foreground="red", font=("Arial", 16)).grid(
                row=6, column=0)
        else:
            listener.port = int(PORT[0])
            listener.redirect = int(var1.get())
            listener.adress = e1.get()
            listener.redirect_port = int(e2.get())
            Label(win, text="").grid(row=3, column=0)

            dictionnary_settings["redirect_active"] = var1.get()
            dictionnary_settings["ip_adress"] = e1.get()
            dictionnary_settings["redirect_port"] = e2.get()
            with open("settings.txt", "w") as f:
                json.dump(dictionnary_settings, f)
            win.destroy()

    win.bind('<Return>', lambda e: button())
    win.bind('<KP_Enter>', lambda e: button())
    b = Button(win, text="Confirm", font=("Arial", 16), command=button)
    b.grid(row=5, column=0, pady=10)

def port_selection(dictionnary_settings, listener, PORT):
    win = Toplevel()
    win.grab_set()
    win.wm_title("Port Selection")
    Label(win, text="Receiving PORT :", font=("Arial", 16)).grid(row=0, column=0, sticky="we", padx=30)
    e = Entry(win, font=("Arial", 16))
    e.insert(0, dictionnary_settings["port"])
    e.grid(row=1, column=0, padx=30)

    def button():
        PORT[0] = e.get()
        if not PORT[0].isdigit() or not 1000 <= int(PORT[0]) <= 65536:
            Message(win, text="The PORT must be an integer between 1000 and 65536", fg="red", font=("Arial", 16)).grid(
                row=3, column=0)
        else:
            listener.socket.close()
            listener.port = int(PORT[0])
            listener.reset()
            Label(win, text="").grid(row=3, column=0)
            dictionnary_settings["port"] = str(PORT[0])
            with open("settings.txt", "w") as f:
                json.dump(dictionnary_settings, f)
            win.destroy()

    win.bind('<Return>', lambda e: button())
    win.bind('<KP_Enter>', lambda e: button())
    b = Button(win, text="Confirm", font=("Arial", 16), command=button)
    b.grid(row=2, column=0, pady=10)

def update_title(top_label1, top_label2, screen):
    top_label1.config(text=session.title_display())
    top_label2.config(text=safetyCarStatusDict[session.safetyCarStatus])
    if session.safetyCarStatus == 4:
        top_label2.config(background="red")
    elif session.safetyCarStatus !=0 or session.anyYellow:
        top_label2.config(background="#FFD700")
    else:
        top_label2.config(background=screen.cget("background"))

def update_frame(LISTE_FRAMES : list[Custom_Frame], PLAYERS_LIST, session):
    for i in range(5):
        LISTE_FRAMES[i].update(PLAYERS_LIST, session)

def update_frame6():
    LISTE_FRAMES[6].update(session)
    