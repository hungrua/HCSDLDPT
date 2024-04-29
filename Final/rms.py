import librosa
import numpy
import csv
from audioFeature import Audio
from scaleData import getMinMax
import json

sr = 20500
# Độ dài khung 25ms
FRAME_SIZE = int(round(sr*0.025))
# Độ dài bước nhảy 10ms
HOP_LENGTH = int(round(sr*0.01))

minmax = [] 


# Năng lượng trung bình của tất cả các frame có độ dài 25ms bước nhảy 10ms
def mean_rootMeanSquare(signal):
    global FRAME_SIZE, HOP_LENGTH
    rms = librosa.feature.rms(y=signal, frame_length= FRAME_SIZE, hop_length= HOP_LENGTH)[0]
    arms = rms.mean()
    return round(arms,9)


# Zero Crossing Rate trung bình của tất cả các frame có độ dài 25ms bước nhảy 10ms
def mean_zeroCrossingRate(signal):
    global FRAME_SIZE, HOP_LENGTH
    zcr = librosa.feature.zero_crossing_rate(y=signal, frame_length= FRAME_SIZE, hop_length= HOP_LENGTH)[0]
    azcr = zcr.mean()
    return round(azcr,9)


#Silent ratio trung bình của tất cả các frame có độ dài 25ms bước nhảy 10ms
def conditions(a,threshold):
    if a < 0 :
        return a>threshold*(-1)
    else :
        return a<threshold
def mean_silenceRatio(signal):
    global FRAME_SIZE, HOP_LENGTH
    amplitude_envelop_threshold = []
    #tính biên bộ lớn nhất trong mỗi frame
    for i in range(0,len(signal),HOP_LENGTH):
        current_frame_amplitude_envelop = max(signal[i:i+FRAME_SIZE])
        amplitude_envelop_threshold.append(current_frame_amplitude_envelop*0.05)
    result = []
    l=0
    for i in range(0,len(signal),HOP_LENGTH):
        count = len([a for a in signal[i:i+FRAME_SIZE] if conditions(a,amplitude_envelop_threshold[l])])
        l= l+1
        result.append(count/FRAME_SIZE)    
    return round(numpy.array(result).mean(),9)

#Bandwidth trung bình của tất cả các frame có độ dài 25ms bước nhảy 10ms
def mean_bandwidth(signal):
    global FRAME_SIZE, HOP_LENGTH
    bw = librosa.feature.spectral_bandwidth(y= signal,n_fft= FRAME_SIZE, hop_length= HOP_LENGTH)
    return round(numpy.array(bw[0]).mean(),9)

#Centroid trung bình của tất cả các frame có độ dài 25ms bước nhảy 10ms
def mean_centroid( signal):
    global FRAME_SIZE, HOP_LENGTH
    ct = librosa.feature.spectral_centroid(y=  signal,n_fft= FRAME_SIZE, hop_length= HOP_LENGTH)
    return round(numpy.array(ct[0]).mean(),9)

#12 giá trị trung bình thuộc tính mfccs
def mfcc_features( signal):
    mfccs = librosa.feature.mfcc(y=signal,hop_length=HOP_LENGTH,n_fft=FRAME_SIZE,n_mfcc=12)
    features = []
    # print(mfccs)
    for i in range(0,len(mfccs)):
        meanFeature = numpy.array(mfccs[i]).mean()
        features.append(round(meanFeature,9))
    return features


def getAllFeature(file):
    name = file
    audio_file = "../Tieng_viet/"+file
    sample,sr = librosa.load(audio_file)
    sample = librosa.effects.preemphasis(sample) #bộ lọc preemphasis
    rms = mean_rootMeanSquare(signal=sample)
    zcr = mean_zeroCrossingRate(signal=sample)
    silence_ratio = mean_silenceRatio(signal=sample)
    bw = mean_bandwidth(signal=sample)
    centroid = mean_centroid(signal=sample)
    mfccs = mfcc_features(signal=sample)
    return Audio(name,rms,zcr,silence_ratio,bw,centroid,mfccs)
    

if __name__ == '__main__':
    audios = []
    data = [
        ['Name', 'RMS', 'ZCR','Silence Ratio','Bandwidth','Centroid',
         'Mfcc1','Mfcc2','Mfcc3','Mfcc4','Mfcc5','Mfcc6',
         'Mfcc7','Mfcc8','Mfcc9','Mfcc10','Mfcc11','Mfcc12']
    ]
    audioObject = []
    with open('VieAudio.csv', mode ='r')as file: 
        csvFile = csv.reader(file) 
        for lines in csvFile: 
            audios.append(lines)
    for audio in audios:
        audioOb = getAllFeature(audio[0])
        data.append(audioOb.getAttributeArr())
        audioObject.append(audioOb)
    csv_file = 'resultVie.csv'

    # Ghi dữ liệu vào file CSV
    # with open(csv_file, mode='w', newline='') as file:
    #     writer = csv.writer(file)
        # writer.writerows(data)   
    for i in range(1,len(data[0])):
        minmax.append(getMinMax(csv_file,data[0][i]))
    # jsonData = []
    for audio in audioObject:
        audio.getScaledArr(minmax)
    print(audioObject[0].getDistance(audioObject[1]))
        # jsonData.append(audio.getScaledAttribute())
    # json_file_path = 'data.json'
    # # Ghi dữ liệu vào file JSON
    # with open(json_file_path, 'w') as json_file:
    #     json.dump(jsonData, json_file, indent=4)
    