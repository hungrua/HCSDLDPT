from audioScaledFeature import ScaledAudio

class Audio:
    def __init__(self, name, rms,zcr,silence_ratio,bw,centroid,mfccs):
        self.name = name
        self.rms = rms
        self.zcr = zcr
        self.silence_ratio= silence_ratio
        self.bw = bw
        self.centroid = centroid
        self.mfccs = mfccs
        self.scaled = []
    
    def getName(self):
        return self.name
    
    def getAttributeArr(self):
        return [self.name,self.rms,self.zcr,self.silence_ratio,self.bw,self.centroid] + self.mfccs
    
    def getScaledArr(self,minmax):
        before = [self.rms,self.zcr,self.silence_ratio,self.bw,self.centroid] + self.mfccs
        after = []
        
        for i in range(len(before)):
            standard = (before[i]-minmax[i]["min"])/(minmax[i]["max"]-minmax[i]["min"])
            if(standard < 10e-8):
                standard = 0.0
            if(1-standard < 10e-8):
                standard= 1.0
            after.append(standard)
        self.scaled  = after
    
    def getScaledAttribute(self):
        return ScaledAudio(self.name,self.scaled)
        
        