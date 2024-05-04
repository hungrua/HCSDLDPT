import json
import pandas as pd
from sklearn.cluster import KMeans
from cluster import Cluster
from audioScaledFeature import ScaledAudio

#Thực hiện phân cụm
def clustering(file):
    
    # Đọc file JSON chứa dữ liệu trước phân cụm
    with open(file) as f:
        data = json.load(f)
    df = pd.DataFrame(data)
    
    
    name = df['Name']
    
    #Thực hiện phân cụm dựa trên các thuộc tính có thể tính toán số học được
    selected_columns = [ "RMS","ZCR","Silence Ratio","Bandwidth","Centroid","Mfcc1",
                        "Mfcc2","Mfcc3","Mfcc4","Mfcc5","Mfcc6","Mfcc7","Mfcc8","Mfcc9","Mfcc10","Mfcc11","Mfcc12"]
    df = df[selected_columns]
    X = df.values
    n_clusters = 12
    kmeans = KMeans(n_clusters=n_clusters)
    kmeans.fit(X)
    # Gán nhãn cụm cho mỗi điểm dữ liệu
    labels = kmeans.labels_
    # Thêm nhãn cụm vào DataFrame
    df['Cụm'] = labels
    
    # Lấy trọng tâm của từng cụm
    centroids = kmeans.cluster_centers_
    result = [] 
    
    #Thêm trường Name 
    df.insert(0,'Name',name)
    
    #Lấy dữ liệu sau khi phân cụm chuyển thành các object dạng JSON để lưu trữ vào file JSON
    for  row in df.iterrows():
        check = 0
        #Duyệt từng cụm
        for cluster in result:
            
            #Nếu tìm thấy audio thuộc cụm vào thì thêm vào
            if(cluster.name ==  str(int(row["Cụm"]))):
                cluster.child.append(toAudioObj(row))
                check =1
                
        #Nếu không thuộc 1 cụm nào thì thực hiện tạo mới 
        if(check==0):
            result.append(Cluster(str(int(row["Cụm"])),centroids[int(row["Cụm"])],[toAudioObj(row)]))
    return result


#Chuyển đổi dữ liệu từ JSON sang Audio Object
def toAudioObj(row):
    scaled = [row['RMS'],row['ZCR'],row['Silence Ratio'],row['Bandwidth'],row['Centroid'],row['Mfcc1'],row['Mfcc2'],row['Mfcc3'],
              row['Mfcc4'],row['Mfcc5'],row['Mfcc6'],row['Mfcc7'],row['Mfcc8'],row['Mfcc9'],row['Mfcc10'],row['Mfcc11'],row['Mfcc12']]
    return ScaledAudio(row['Name'],scaled)
            

if __name__ == '__main__':
    #Kết quả phân cụm từ file chưa phân cụm
    result = clustering('data.json')
    jsonData = []
    for rs in result:
        jsonData.append(rs.toJson())
    
    #Ghi kết quả phân cụm vào file 
    json_file_path = 'clusters.json'
    # Ghi dữ liệu vào file JSON
    with open(json_file_path, 'w') as json_file:
        json.dump(jsonData, json_file, indent=4)
    
    