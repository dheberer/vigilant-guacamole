from csv_utils import get_all_files, read_csv_file

"""
Weather task specific
"""

# returns row (represented as dict) that is coldest in rows
def get_min_for_table(rows: list, field: str) -> dict:
    error = ["-9999", "N/A"]
    lowest_row = None

    for r in rows:
        if r[field] in error:
            continue
        f = float(r[field])
        if lowest_row == None or f < float(lowest_row[field]):
            lowest_row = r
    
    return lowest_row

# returns average value for the table, error row counts as 0
def get_avg_for_table(rows: list, field: str) -> float:
    error = ["-9999", "N/A"]
    total = 0.0

    for r in rows:
        if r[field] in error:
            continue
        total += float(r[field])

    return total / len(rows)

def file_with_min_record(files: list, field: str) -> str:
    lowest_seen = 5000.0
    lowest_file = ""

    for f in files:
        cols, rows = read_csv_file(f)
        row = get_min_for_table(rows, field)
        if float(row[field]) < lowest_seen:
            lowest_seen = float(row[field])
            lowest_file = f

    fh = open(f, "r")
    lines = fh.readlines()
    fh.close()

    print("File with lowest row was " + lowest_file)
    print("Minimum observed " + field + " was " + str(lowest_seen))
    for l in lines:
        print (l)
    
    return lowest_file 
    
def main():
    root = "nc_weather/2013"
    files = get_all_files(root)

    f = file_with_min_record(files, "TemperatureF")
    print (f)

    # cols, rows = read_csv_file("nc_weather/2013/weather-2013-08-10.csv")
    # a = get_avg_for_table(rows, "TemperatureF")
    # print("Average for file was " + str(a))

main()