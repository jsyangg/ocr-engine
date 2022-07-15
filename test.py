import textract_table
import textract_doctext
import boto3
import os
import glob
import shutil 
import pickle
import json
from trp import Document
from tqdm import tqdm

# textract_table
# textract_doctext
# textract_
# textract_tabletransorm


data_dir = 'D:/snuh_bmi/PFT-OCR/PFT_Raw/process_data/'
rawdata_dir = data_dir + 'test_data_2/' # data_dir + 'actual_process/'
save_dir = data_dir + 'test_data_2_processed/'

os.chdir(rawdata_dir)
   
for file in tqdm(os.listdir(rawdata_dir)):
    os.mkdir(save_dir + file[:-4])
    
    save_path = save_dir + file[:-4] + '/'
    
    textract_table.raw_table_csv(file, save_path)
    textract_doctext.read_doc(file, save_path)
    
    # print(f'{file} extraction completed...')

print('Raw data extraction completed.')
print('Preprocessing each data (Rawtext, Table).')

for file in tqdm(os.listdir(rawdata_dir)):
    os.chdir('D:\snuh_bmi\PFT-OCR\PFT_Raw\process_data\test_data_2_processed/' + file[:-4] + '/')
    # actual_processed
    textract_table.generate_clean_csv(file[:-4] + '_table.csv')

    
    
    


