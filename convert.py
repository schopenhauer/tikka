#!/usr/bin/env python

import tika
import os
import traceback
import sys
import json

tika.initVM()
from tika import parser

def clean(str):
    return '\r\n'.join([x for x in str.splitlines() if x.strip()])

def clear_folder(folder):
    files = os.listdir(folder)
    for file in files:
        os.remove(os.path.join(folder, file))

def dump(file, data):
    f = open(file, 'w')
    f.write(data)
    f.close()

content_extension = '.txt'
metadata_extension = '.metadata.txt'

input_folder = './input'
output_folder = './output'

def start():

    print('Cleaning up...')
    clear_folder(output_folder)

    files = os.listdir(input_folder)
    for file in files:
        target_file = os.path.join(input_folder, file)

        parsed = parser.from_file(target_file)
        content = parsed['content']
        metadata = parsed['metadata']

        print('Converting:', file, '(' + metadata['xmpTPg:NPages'] + ' pages)')

        dump(os.path.join(output_folder, file) + content_extension, clean(content))
        dump(os.path.join(output_folder, file) + metadata_extension, json.dumps(metadata))

    print('Done.')

if __name__ == '__main__':
    try:
        start()
    except KeyboardInterrupt:
        print('Shutdown requested... exiting.')
    except Exception:
        traceback.print_exc(file=sys.stdout)

    sys.exit(0)
