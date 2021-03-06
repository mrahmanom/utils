import os
import chardet
import glob
import sys
import argparse

def list_files(path):
    result = []
    if(os.path.exists(path)):
        for root, directories, filenames in os.walk(path):
            for filename in filenames:
                if(filename.endswith(".sql")):
                    result.append(os.path.join(root, filename))
    return result

def get_files_with_utf16_encoding(path):
    files = list_files(path)
    resultSet = {}
    for file in files:
        with open(file,'rb') as f:
            data = f.read()
            result = chardet.detect(data)
            resultSet[file] = result['encoding']

    filtered_dict = {k:v for k,v in resultSet.items() if v is not None and 'UTF-16' in v}
    return filtered_dict

def convert_files_to_utf8(file):
    with open(file, 'rb') as f:
        file_data = f.read()

    with open(file, 'w+b') as f:
        f.write(file_data.decode('utf-16').encode('utf-8'))

def process(path):
    print("working on path" + path)
    files = get_files_with_utf16_encoding(path)
    print("got list of files")
    for f in files:
        convert_files_to_utf8(f)
    print("exiting script")


if __name__=="__main__":
    parser = argparse.ArgumentParser(description="Convert all sql scripts that are encoded in UTF-16 to UTF-8")
    parser.add_argument('path', type=str, help="Path to parse files")
    args = parser.parse_args()
    process(args.path)