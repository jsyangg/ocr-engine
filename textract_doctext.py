import boto3

def read_doc(doc_name, save_dir):

    # Read document content
    with open(doc_name, 'rb') as document:
        imageBytes = bytearray(document.read())

    # Amazon Textract client
    textract = boto3.client('textract')

    # Call Amazon Textract
    response = textract.detect_document_text(Document={'Bytes': imageBytes})
    
    output_file = f'{doc_name[:-4]}_rawtext.txt'
    
    with open(save_dir + output_file, 'wt', encoding='utf-8') as fout:
        for item in response["Blocks"]:
            if item["BlockType"] == "LINE":
                fout.write(item["Text"] + '\n')

    # print('TXT OUTPUT FILE : ', output_file)
    
def get_Temp(input : dir):
    
    with open(input, 'rt', encoding='utf-8') as txt:
        for line in txt:
            if 'Temp' in line:
                Temp = {line[:4], line[-3:-1]}
                return Temp
            
def get_PBar(input : dir):
    
    with open(input, 'rt', encoding='utf-8') as txt:
        for line in txt:
            if 'PBar' in line:
                PBar = {line[:4], line[-3:-1]}
                return PBar
            
