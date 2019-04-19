import pandas as pd 
import json
import os
from feature_extraction import extract
import sys

window_size = 50
step_size = 10

mode = sys.argv[1]
# print(mode)

dir_path = 'Datasets_' + mode + '/'
dir = os.listdir(dir_path)
result = []
# print(dir)
for csv_file in dir:
    dataframe = pd.read_csv(os.path.join(dir_path, csv_file))
    dataset = dataframe.values
    print(dataset)
    for row in range(int((len(dataset) - window_size) / step_size)):
        processed = extract(dataset[row*step_size:row*step_size+window_size])
        if(len(dataset[0]) != 10):      
                print('There are errors in this file: ' + csv_file)
        processed.append(dataset[row*step_size][-1])
        # print(processed)
        result.append(processed)

df = pd.DataFrame(result)
df.to_csv('processed_'+ mode +'.csv', header=0, index=False)