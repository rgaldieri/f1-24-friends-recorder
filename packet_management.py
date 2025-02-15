from Session import Session
from DataMemory import DataMemory
from dictionnaries import *
from DB_Connection import *
import json
import math
import time
import traceback

session: Session = Session()
TT_data : DataMemory = DataMemory()

def n_update_session(packet, header, *args):
    # Right now i only  care about tracks, I think
    if(session.check_track_change(packet)):
        TT_data.reset()

def n_time_trial(packet, header):
    #Checking previous existing laps
    if((not TT_data.bestTimeInitialized) and TT_data.playerInitialized and session.track != -1):
        #Initializing data
        if(packet.m_personalBestDataSet.m_lap_time_in_ms > 0):
            TT_data.bestLapTime = packet.m_personalBestDataSet.m_lap_time_in_ms
            print("Previous recorded best time is " + str(TT_data.bestLapTime))
            TT_data.setBestTimeStruct(packet.m_personalBestDataSet)
            update_best_time_if_faster(
                    TT_data.playerName, 
                    session.track, 
                    packet.m_personalBestDataSet.m_lap_time_in_ms, 
                    packet.m_personalBestDataSet.m_sector1_time_in_ms, 
                    packet.m_personalBestDataSet.m_sector2_time_in_ms, 
                    packet.m_personalBestDataSet.m_sector3_time_in_ms)
        else:
            print("No Best Time Recorded")
        TT_data.bestTimeInitialized = True
    # per-packet check
    if(TT_data.playerInitialized and TT_data.bestTimeInitialized):
        # This happens the first time a best time happens on a circuit
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
        # This executes if a new personal best is detected and one existed
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
    if(not TT_data.playerInitialized and header.m_player_car_index != -1):
        #Initializing data
        pName = packet.m_participants[header.m_player_car_index].m_name.decode("utf-8") 
        TT_data.initialize(header.m_player_car_index, pName)
        print("Initializing player " + pName+ " with ID = " + str(header.m_player_car_index))
        TT_data.playerInitialized = True

def nothing(packet, header):# Packet 8, 9, 11, 12, 13
    pass
