# csv expected in format
# 1st row - column names
# subsequent rows - comma separated values
from os import listdir
from os.path import isfile, join

"""
produce list of columns in order
"""
def read_cols(line: str) -> list :
    return line.split(",")

"""
produce a prop bag given the columns
"""
def read_row(line: str, cols: list) -> dict :
    ret_val = {}
    cells = line.split(",")
    assert len(cols) == len(cells)
    for i in range(len(cells)):
        ret_val[cols[i]] = cells[i]
    return ret_val

"""
returns the column names as a list and then all 
the subsequent rows as dicts with keys from the
column name list
"""
def read_csv_file(filename: str) -> (list, list):
    rows = []
    file = open(filename, "r")
    col_names = read_cols(file.readline())
    lines = file.readlines()
    file.close()
    for line in lines:
        rows.append(read_row(line))
    
    return (col_names, rows)

def get_all_files(root: str) -> list:
    onlyfiles = [f for f in listdir(root) if isfile(join(root, f))]
    return onlyfiles
    
def main():
    
    read_csv_file("")
main()