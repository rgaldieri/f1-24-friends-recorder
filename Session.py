class Session:
    def __init__(self):
        self.currentLap = 0
        self.track = -1
        self.idxBestLapTime = -1
        self.bestLapTime = 5000
        self.nb_players = 22
        self.circuit_changed = False

    def update_track(self, track_id):
        self.track = track_id

    def get_track_by_id(self, number):
        match number:
            case 0:
                return "Melbourne"
            case 1:
                return "France"
            case 2:
                return "Shanghai"
            case 3:
                return "Bahrain"
            case 4:
                return "Catalunya"
            case 5:
                return "Monaco"
            case 6:
                return "Montreal"
            case 7:
                return "Silverstone"
            case 8:
                return "Hockenheim"
            case 9:
                return "Hungaroring"
            case 10:
                return "Spa"
            case 11:
                return "Monza"
            case 12:
                return "Singapore"
            case 13:
                return "Suzuka"
            case 14:
                return "AbuDhabi"
            case 15:
                return "Texas"
            case 16:
                return "Brazil"
            case 17:
                return "Austria"
            case 18:
                return "Sochi"
            case 19:
                return "Mexico"
            case 20:
                return "Baku"
            case 21:
                return "Sakhir_Short"
            case 22:
                return "Silverstone_Short"
            case 23:
                return "Texas_Short"
            case 24:
                return "Suzuka_Short"
            case 25:
                return "Hanoi"
            case 26:
                return "Zandvoort"
            case 27:
                return "Imola"
            case 28:
                return "Portimão"
            case 29:
                return "Jeddah"
            case 30:
                return "Miami"
            case 31:
                return "LasVegas"
            case 32:
                return "Losail"

    def check_track_change(self, packet):
        if(self.track is not packet.m_track_id):
            print("Track " + self.get_track_by_id(packet.m_track_id) + " Initialized with ID " + str(packet.m_track_id))
            self.track = packet.m_track_id
            return True
        return False
