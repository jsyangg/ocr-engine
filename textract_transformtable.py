from xmlrpc.client import Boolean
import pandas as pd
import os
import itertools
from textract_doctext import get_PBar, get_Temp
'''
textract_transformtable.py
changes the file form (dataframe table -> one-row dataframe).
'''

# pre-processed 된 테이블을 받아서 하나의 긴 열로 출력해준다. 
# change directory? -> 출력을 cwd로 해주기 때문에 iteration 마다 os.chdir() 해줘야한다. 
def table_transformer(input_df, file_name): 
    input_df_data = []
    input_df_col = []
    
    for x in range(1, len(input_df)):
        for y in range(2, len(input_df.columns)):
            input_df_col.append(f"{input_df.iloc[x,0]} ({input_df.iloc[x,1]}) {input_df.iloc[0,y]}")
            input_df_data.append(input_df.iloc[x,y])
    
    input_df_col.insert(0, 'Temp')
    input_df_data.insert(0, get_Temp['Temp'])
    input_df_col.insert(0, 'PBar')
    input_df_data.insert(0, get_PBar['PBar'])
    input_df_col.insert(0, 'filename')
    input_df_data.insert(0, file_name[:-4])
    
    df1 = pd.DataFrame(columns=input_df_col)
    df1.loc[0] = input_df_data
    df1.to_excel(f'{file_name[:-4]}.xlsx')
    return 


# strip each elements. ('Spirometry ' -> 'Spirometry')
def table_preprocess(input):
    df_file = pd.read_csv(input)

    for i, j in itertools.product(range(df_file.shape[0]), range(df_file.shape[1])):
        if type(df_file.iloc[i,j]) == str:
            df_file.iloc[i,j] = df_file.iloc[i,j].strip()
            
    return df_file
       