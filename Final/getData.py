import librosa
import numpy
import csv
from audioFeature import Audio
from scaleData import getMinMax
import json
from clustering import clustering
from audioScaledFeature import ScaledAudio
from getAudioFeature import getAllFeature
sr = 20500
# Độ dài khung 25ms
FRAME_SIZE = int(round(sr*0.025))
# Độ dài bước nhảy 10ms
HOP_LENGTH = int(round(sr*0.01))


if __name__ == '__main__':
    audios = []
    data = [
        ['Name', 'RMS', 'ZCR','Silence Ratio','Bandwidth','Centroid',
         'Mfcc1','Mfcc2','Mfcc3','Mfcc4','Mfcc5','Mfcc6',
         'Mfcc7','Mfcc8','Mfcc9','Mfcc10','Mfcc11','Mfcc12']
    ]
    audioObject = []
    
    # Đọc tên file được tổng hợp trong file csv
    with open('VieAudio.csv', mode ='r')as file: 
        csvFile = csv.reader(file) 
        for lines in csvFile: 
            audios.append(lines)
    for audio in audios:
        audioOb = getAllFeature(audio[0])
        data.append(audioOb.getAttributeArr())
        audioObject.append(audioOb)
    csv_file = 'resultVie.csv'
    # Ghi dữ liệu các thuộc tính của audio vào file CSV
    with open(csv_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(data)
        
    #Lấy ra các dữ liệu để chuẩn hóa minmax    
    minmax = getMinMax(csv_file)
    jsonData = []

    #Thực hiện scale minmax dữ liệu
    for audio in audioObject:
        audio.getScaledArr(minmax)
        scaledAudio = audio.getScaledAttribute()
        jsonData.append(scaledAudio.toJSON())

    #Ghi dữ liệu đã được scale vào json
    json_file_path = 'data.json'

    with open(json_file_path, 'w') as json_file:
        json.dump(jsonData, json_file, indent=4)