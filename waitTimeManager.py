import random
LONG_TIME_MS = 1000*60*60*12

class waitTimeManager:
    pdf = None
    cdf = None
    totalWait = 0
    def __init__(self, mix: dict) -> None:
        pdf = []
        for key in mix.keys():
            pdf.append([key, LONG_TIME_MS])
        self.pdf = pdf
        self.__updateWaitTimeCDF()


    def increaseWaitTimes(self, increase_ms, played_track_uri):
        for pair in self.pdf:
            if pair[0] != played_track_uri:
                pair[1] += increase_ms
            else:
                pair[1] = 0
        print("PDF: ", self.pdf, "\n")
        self.__updateWaitTimeCDF()

    # update after pdf changes.
    def __updateWaitTimeCDF(self):
        cdf: list[list] = []
        quantile = 0 #integer, not percent.
        for pair in self.pdf:
            quantile += pair[1]
            cdf.append([pair[0], quantile])
        self.cdf = cdf
        self.totalWait = quantile
        print("CDF: ", cdf, "\n")
        return
    
    def getRandomSong(self):
        x = random.randrange(0, self.totalWait)
        print(x)
        valuesList = [pair[1] for pair in self.cdf]
        ind = self.__indexOfSmallestOver(x, valuesList)
        return self.cdf[ind][0]
        # binary search through CDF.

    # search for index of the largest number less than x.
    def __indexOfSmallestOver(self, x, valuesList):
        if valuesList[len(valuesList)-1] < x:
            return -1
        n = len(valuesList)
        lo = 0
        hi = n - 1
        mid = (hi+lo)//2
        while lo <= hi:
            if valuesList[mid] >= x:
                if hi == mid:
                    break
                hi = mid
            else:
                lo = mid + 1
            mid = (hi+lo)//2
        if valuesList[lo] >= x:
            return lo
        return hi


