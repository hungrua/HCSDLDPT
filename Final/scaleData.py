import numpy as np
from audioFeature import Audio
import pandas as pd
def getMinMax(file_csv,columnName):
    df = pd.read_csv(file_csv)
    min_value = df[columnName].min()
    max_value = df[columnName].max()
    return {
        "min" : min_value,
        "max": max_value
    }
        