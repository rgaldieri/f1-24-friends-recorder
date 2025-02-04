class DataMemory:
    def __init__(self):
        self.reset()

    def initialize(self, alltime_best):
        self.bestLapTime = alltime_best
        self.initialized = True

    def setBestTimeStruct(self, best_struct):
        self.bestTimeStruct = best_struct

    def reset(self):
        self.initialized = False
        self.bestLapTime = -1
        self.playerName = ""
        self.playerIndex = -1
        self.bestTimeStruct = None
