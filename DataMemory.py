class DataMemory:
    def __init__(self):
    	self.initialized = False

    def initialize(self, alltime_best):
    	self.alltime_best_lap = alltime_best
    	self.initialized = True
    	print("Init")