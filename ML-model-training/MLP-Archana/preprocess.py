import pandas as pd 
import json
import os
from feature_extraction import extract

window_size = 50
step_size = 10  #80% overlap seems to work for us

dir = os.listdir('./13april_data/')
result = []
#print(dir)
for csv_file in dir:
    dataframe = pd.read_csv(os.path.join('13april_data', csv_file))
    dataset = dataframe.values
    #print(dataset)
    for row in range(int((len(dataset) - window_size) / step_size)):
        processed = extract(dataset[row*step_size:row*step_size+window_size])
        processed.append(dataset[row][-1])
        # print(processed)
        #print(len(dataset))
        result.append(processed)

df = pd.DataFrame(result)
df.to_csv('preprocess_17april_logout.csv', header=0)
