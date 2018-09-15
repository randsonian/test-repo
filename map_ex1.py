# -*- coding: utf-8 -*-
"""
Created on Mon Sep  3 11:42:59 2018

@author: juan
"""

import os, mmap, json

input_files_location = r'C:\Users\juan\Documents\dev\benefits_input'
output_location = r'C:\Users\juan\Documents\dev\benefits_output'
os.chdir(input_files_location)

def parse_record(record):
    element = ''
    for c in record:
        if c != '|':
            element += c
        elif c == '|':
            break
    return(element)

## This is not used, get_record is used instead
def parse_mmap(map_file, index, separator):
    record = []
    field = ''
    print(index)
    while True:
        try:
            ch = map_file[index]
        except IndexError:
            record.append(field)
            return(tuple(record))
        if ch != separator and ch != 13:
            field = field + chr(ch)
        else:
            record.append(field)
            field = ''
            if ch == 13: break
        index += 1
    return(tuple(record))

def get_header(map_file, separator):
    header = []
    field = ''
    index = 0
    while True:
        if map_file[index] != separator and map_file[index] != 13:
            field = field + chr(map_file[index])
        else:
            header.append(field)
            field = ''
            if map_file[index] == 13: break
        index += 1
    return(header)

def get_record(map_file, index, separator):
    record = []
    field = ''
    print(index)
    while True:
        try:
            if map_file[index] != separator and map_file[index] != 13:
                field = field + chr(map_file[index])
            else:
                record.append(field)
                field = ''
                if map_file[index] == 13: break
            index += 1
        except IndexError:
            record.append(field)
            break
    return(record)


def memory_map(filename, access=mmap.ACCESS_WRITE):
    size = os.path.getsize(filename)
    fd = os.open(filename, os.O_RDWR)
    return mmap.mmap(fd, size, access=access)


def search_by_BAN(ban, map_file, index):
    map_file.seek(index)
    return(map_file.find(ban.encode()))

    
## Read input files in input_list

ban='23399231'
separator = 124

with memory_map('bi_002.txt') as m:
    ## 'm' file is similar to a bytearray object
    ## you can index them, slice them, search them with regular expressions and the like
    print(m[2:23].decode())
    BAN_index = []
    mind = -1
    while True:
        mind = search_by_BAN(ban, m, mind+1)
        if mind==-1:
            break
        else:
            BAN_index.append(mind)

    header = get_header(m, separator)
 
    ban_data = []
    for rind in BAN_index:
        ban_data.append(dict(zip(header, get_record(m, rind, separator))))
        
    
## ban_data_dict = dict(ban_data)    
my_first_json = json.dumps(ban_data)
print(my_first_json)


