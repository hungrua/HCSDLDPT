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
    def __str__(self):
        return self.name
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
        key = ['RMS', 'ZCR','Silence Ratio','Bandwidth','Centroid',
         'Mfcc1','Mfcc2','Mfcc3','Mfcc4','Mfcc5','Mfcc6',
         'Mfcc7','Mfcc8','Mfcc9','Mfcc10','Mfcc11','Mfcc12']
        jsonOb = {}
        jsonOb['Name']= self.name
        for i in range(len(key)):
            jsonOb[key[i]] = self.scaled[i] 
        return jsonOb
    def getDistance(self,audio):
        squareTotal  = 0
        attr1 = self.scaled
        attr2 = audio.scaled
        for i in range(len(attr1)):
            squareTotal+= (attr1[i]-attr2[i])**2
        distance = round(squareTotal**0.5,9)
        return distance
        
        