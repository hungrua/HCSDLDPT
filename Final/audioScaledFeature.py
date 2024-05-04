class ScaledAudio:
    def __init__(self, name,scaled):
        self.name = name
        self.rms = scaled[0]
        self.zcr = scaled[1]
        self.silence_ratio= scaled[2]
        self.bw = scaled[3]
        self.centroid = scaled[4]
        self.mfcc1 = scaled[5]
        self.mfcc2 = scaled[6]
        self.mfcc3 = scaled[7]
        self.mfcc4 = scaled[8]
        self.mfcc5 = scaled[9]
        self.mfcc6 = scaled[10]
        self.mfcc7 = scaled[11]        
        self.mfcc8 = scaled[12]
        self.mfcc9 = scaled[13]
        self.mfcc10 = scaled[14]
        self.mfcc11 = scaled[15]
        self.mfcc12 = scaled[16]
        self.allFeature = scaled
        
    def toJSON(self):
        key = ['RMS', 'ZCR','Silence Ratio','Bandwidth','Centroid',
         'Mfcc1','Mfcc2','Mfcc3','Mfcc4','Mfcc5','Mfcc6',
         'Mfcc7','Mfcc8','Mfcc9','Mfcc10','Mfcc11','Mfcc12']
        jsonOb = {}
        jsonOb['Name']= self.name
        for i in range(len(key)):
            jsonOb[key[i]] = self.allFeature[i] 
        return jsonOb

    def distance(self,another):
        totalSquare = 0
        for i in range(len(self.allFeature)):
            totalSquare += (self.allFeature[i] - another.allFeature[i])**2
        return totalSquare**0.5 