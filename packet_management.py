from Session import Session
from DataMemory import DataMemory
from Player import Player
from dictionnaries import *
from DB_Connection import *
import json
import math
import time
from ttkbootstrap import Toplevel, LEFT, Entry, IntVar, Label
from tkinter import Message, Checkbutton, Button
from Custom_Frame import Custom_Frame
import traceback

session: Session = Session()
TT_data : DataMemory = DataMemory()

PAGES_LIST = []

def n_update_session(packet, header, *args):
    # Right now i only  care about tracks, I think
    if(session.check_track_change(packet)):
        TT_data.reset()

def n_time_trial(packet, header):
    if(not TT_data.initialized):
        #Initializing data
        TT_data.playerIndex = header.m_player_car_index
        if(packet.m_personalBestDataSet.m_lap_time_in_ms > 0):
            TT_data.bestLapTime = packet.m_personalBestDataSet.m_lap_time_in_ms
            print("Previous recorded best time is " + str(TT_data.bestLapTime))
            TT_data.setBestTimeStruct(packet.m_personalBestDataSet)
        else:
            print("No Best Time Recorded")
        TT_data.initialized = True
    # per-packet check
    if(TT_data.bestLapTime == -1):
        if(packet.m_personalBestDataSet.m_lap_time_in_ms > 0 and packet.m_personalBestDataSet.m_valid == 1):
            TT_data.bestLapTime = packet.m_playerSessionBestDataSet.m_lap_time_in_ms
            TT_data.setBestTimeStruct(packet.m_playerSessionBestDataSet)
            print("First Best on cirucit:" + str(TT_data.bestLapTime))
            add_best_time(TT_data.playerName,
                session.track,
                packet.m_playerSessionBestDataSet.m_lap_time_in_ms, 
                packet.m_playerSessionBestDataSet.m_sector1_time_in_ms, 
                packet.m_playerSessionBestDataSet.m_sector2_time_in_ms, 
                packet.m_playerSessionBestDataSet.m_sector3_time_in_ms)
    elif(packet.m_personalBestDataSet.m_lap_time_in_ms < TT_data.bestLapTime and packet.m_personalBestDataSet.m_lap_time_in_ms > 0 and packet.m_personalBestDataSet.m_valid == 1):
        TT_data.bestLapTime = packet.m_playerSessionBestDataSet.m_lap_time_in_ms
        TT_data.setBestTimeStruct(packet.m_playerSessionBestDataSet)
        print("New Best:" + str(TT_data.bestLapTime))
        add_best_time(TT_data.playerName,
            session.track,
            packet.m_playerSessionBestDataSet.m_lap_time_in_ms, 
            packet.m_playerSessionBestDataSet.m_sector1_time_in_ms, 
            packet.m_playerSessionBestDataSet.m_sector2_time_in_ms, 
            packet.m_playerSessionBestDataSet.m_sector3_time_in_ms)

def n_update_participants(packet, header):
    if(TT_data.playerIndex > -1 and TT_data.playerName == ""):
        TT_data.playerName = packet.m_participants[TT_data.playerIndex].m_name.decode("utf-8") 
        print("Green light " + str(TT_data.playerName) + ", GO GO GO!")
        if(TT_data.bestLapTime > 0 and session.track != -1):
            update_best_time_if_faster(TT_data.playerName, 
                session.track, 
                TT_data.bestTimeStruct.m_lap_time_in_ms,
                TT_data.bestTimeStruct.m_sector1_time_in_ms, 
                TT_data.bestTimeStruct.m_sector2_time_in_ms, 
                TT_data.bestTimeStruct.m_sector3_time_in_ms
            )

def nothing(packet, header):# Packet 8, 9, 11, 12, 13
    pass

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