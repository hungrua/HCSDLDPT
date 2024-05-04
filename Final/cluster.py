from audioScaledFeature import ScaledAudio
class Cluster:
    def __init__(self,name,centroid,child):
        self.name = name
        self.centroid = ScaledAudio(name,centroid)
        self.child = child
        
    def getChildObj(self):
        childArr = []
        for child in self.child:
            childArr.append(child.toJSON())
        return childArr
    
    def toJson(self):
        jsonOb = {}
        jsonOb['Name']= self.name
        jsonOb['Centroid'] = self.centroid.toJSON()
        jsonOb['child'] = self.getChildObj()
        return jsonOb
        