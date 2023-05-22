class ScreenMaster:
    def __init__(self):
        self.screenID = 0
        self.prevScreenID = self.screenID
        self.screenMeanings = {
            0: "Joining screen",
            1: "Lobby",
            2: "Loading",
            10: "Game"
        }

        self.uponScreenChange = {

        }
        self.screenFunc = {

        }

    def tick(self):
        if self.screenID != self.prevScreenID:
            if self.screenID in self.uponScreenChange.keys():
                self.uponScreenChange[self.screenID]()

        self.prevScreenID = self.screenID
        if self.screenID in self.screenFunc.keys():
            self.screenFunc[self.screenID]()



    def addChangeFunc(self, screenID, func):
        self.uponScreenChange[screenID] = func

    def addScreenFunc(self, screenID, func):
        self.screenFunc[screenID] = func