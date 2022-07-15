import webbrowser, os
import json
import boto3
import io
from io import BytesIO
import sys
from pprint import pprint
import pandas as pd


def get_rows_columns_map(table_result, blocks_map):
    rows = {}
    for relationship in table_result['Relationships']:
        if relationship['Type'] == 'CHILD':
            for child_id in relationship['Ids']:
                cell = blocks_map[child_id]
                if cell['BlockType'] == 'CELL':
                    row_index = cell['RowIndex']
                    col_index = cell['ColumnIndex']
                    if row_index not in rows:
                        # create new row
                        rows[row_index] = {}
                        
                    # get the text value
                    rows[row_index][col_index] = get_text(cell, blocks_map)
    return rows


def get_text(result, blocks_map):
    text = ''
    if 'Relationships' in result:
        for relationship in result['Relationships']:
            if relationship['Type'] == 'CHILD':
                for child_id in relationship['Ids']:
                    word = blocks_map[child_id]
                    if word['BlockType'] == 'WORD':
                        text += word['Text'] + ' '
                    if word['BlockType'] == 'SELECTION_ELEMENT':
                        if word['SelectionStatus'] =='SELECTED':
                            text +=  'X '    
    return text


def get_table_csv_results(file_name):

    # os.chdir(path)
    data_dir = 'D:/snuh_bmi/PFT-OCR/PFT_Raw/process_data/actual_process_mod/'
    os.chdir(data_dir)
    with open(data_dir + file_name, 'rb') as file:
        img_test = file.read()
        bytes_test = bytearray(img_test)
        # print('Image loaded', file_name)

    # process using image bytes
    # get the results
    client = boto3.client('textract')

    response = client.analyze_document(Document={'Bytes': bytes_test}, FeatureTypes=['TABLES'])

    # Get the text blocks
    blocks=response['Blocks']
    # pprint(blocks)

    blocks_map = {}
    table_blocks = []
    for block in blocks:
        blocks_map[block['Id']] = block
        if block['BlockType'] == "TABLE":
            table_blocks.append(block)

    if len(table_blocks) <= 0:
        return "<b> NO Table FOUND </b>"

    csv = ''
    for index, table in enumerate(table_blocks):
        csv += generate_table_csv(table, blocks_map, index +1)
        csv += '\n\n'

    return csv

def generate_table_csv(table_result, blocks_map, table_index):
    rows = get_rows_columns_map(table_result, blocks_map)

    table_id = 'Table_' + str(table_index)
    
    # get cells.
    csv = 'Table: {0}\n\n'.format(table_id)

    for row_index, cols in rows.items():
        
        for col_index, text in cols.items():
            csv += '{}'.format(text) + ","
        csv += '\n'
        
    csv += '\n\n\n'
    return csv

def raw_table_csv(file_name, save_dir):
    # os.chdir(save_dir)
    table_csv = get_table_csv_results(file_name)

    output_file = f'{file_name[:-4]}_table.csv'

    # replace content
    with open(save_dir + output_file, "wt") as fout:
        fout.write(table_csv)

    # show results
    # print('CSV OUTPUT FILE: ', output_file)

def generate_clean_csv(file_name):
 
    with open(file_name, 'rt', encoding='utf-8') as f:
        Lines = f.readlines()
    
    for i in range(len(Lines)):
        Lines[i] = Lines[i].strip()

    for word in Lines:
        if word in ['Table: Table_1']:
            num1 = Lines.index(word)

        if word in ['Table: Table_2']:
            num2 = Lines.index(word)

    try : 
        num2
    except NameError:
        output_file = f'{file_name[:-4]}_cleantable.txt'
        
        list1 = Lines[num1+1:]
        with open(output_file, 'w', encoding='utf-8') as fout:
            for x in list1:
                fout.write(x + '\n')
        pd.read_csv(output_file).to_csv(f'{file_name[:-4]}_cleantable.csv')
        
        return 
        
    else:
        list1 = Lines[num1+1:num2]
        list2 = Lines[num2+1:]
        output_file_1 = f'{file_name[:-4]}_cleantable_1.txt'
        output_file_2 = f'{file_name[:-4]}_cleantable_2.txt'
        
        with open(output_file_1, 'w', encoding='utf-8') as fout_1:
            for x in list1:
                fout_1.write(x + '\n')
        
        with open(output_file_2, 'w', encoding='utf-8') as fout_2:
            for x in list2:
                fout_2.write(x + '\n')
        
        pd.read_csv(output_file_1).to_csv(f'{file_name[:-4]}_cleantable_1.csv')
        pd.read_csv(output_file_2).to_csv(f'{file_name[:-4]}_cleantable_2.csv')
        
        return

if __name__ == "__main__":
    file_name = sys.argv[1]
    raw_table_csv(file_name)