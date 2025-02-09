class DataMemory:
    def __init__(self):
        self.reset()
        self.playerInitialized = False
        self.playerName = ""
        self.playerIndex = -1

    def initialize(self, playerIndex, playerName):
        self.playerIndex = playerIndex
        self.playerName = playerName
        self.playerInitialized = True

    def setBestTimeStruct(self, best_struct):
        self.bestTimeStruct = best_struct

    def reset(self):
        self.bestTimeInitialized = False
        self.bestLapTime = -1
        self.bestTimeStruct = None
