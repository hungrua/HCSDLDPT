import numpy as np
from audioFeature import Audio
import pandas as pd
comlumns = [ 'RMS', 'ZCR','Silence Ratio','Bandwidth','Centroid',
         'Mfcc1','Mfcc2','Mfcc3','Mfcc4','Mfcc5','Mfcc6',
         'Mfcc7','Mfcc8','Mfcc9','Mfcc10','Mfcc11','Mfcc12']
def getMinMax(file_csv):
    minmax = []
    df = pd.read_csv(file_csv)
    for columnName in comlumns:
        min_value = df[columnName].min()
        max_value = df[columnName].max()
        minmax.append( {
            "min" : min_value,
            "max": max_value
        })
    return minmax
        