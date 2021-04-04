from csv_utils import read_csv_file, get_all_files

# Each year has a flat table of name, gender, and count for a given name
# Been tasked to write some functions to analyze the data and produce
# basic stats

# these flat files are already ordered by gender, count so we're going
# to take advantage of this fact

def total_births(filename: str) -> None:
    _cols, rows = read_csv_file(filename, False)
    f_births = 0
    m_births = 0
    f_names = 0
    m_names = 0

    for r in rows:
        if r["1"] == "F":
            f_births += int(r["2"])
            f_names += 1
        else:
            m_births += int(r["2"])
            m_names += 1
    
    print("Counted file " + filename)
    print("Total births for the files is: " + str(f_births + m_births))
    print("Female births is: " + str(f_births))
    print("Male births is: " + str(m_births))
    print("Total name count is: " + str(f_names + m_names))
    print("Female name count is: " + str(f_names))
    print("Male name count is: " + str(m_names))

# returns -1 in case of error
def get_rank(year: int, name: str, gender: str) -> int:
    if year < 1880 or year > 2014:
        print("No data available for this year.")
        return -1
    
    rank = 1
    _cols, rows = read_csv_file("us_babynames/us_babynames_by_year/yob" + str(year) + ".csv", False)
    found = False
    for r in rows:
        if gender != r["1"]:
            continue
        if name == r["0"]:
            found = True
            break
        
        rank += 1
    
    if found:
        return rank
    else:
        print("WARNING: Name " + name + " not found in that year")
        return -1

def get_name(year: int, rank: int, gender: str) -> str:
    if year < 1880 or year > 2014 or rank < 1:
        print("No data available for this year or rank.")
        return ""
    
    seen = 0
    _cols, rows = read_csv_file("us_babynames/us_babynames_by_year/yob" + str(year) + ".csv", False)
    for r in rows:
        if gender != r["1"]:
            continue

        seen += 1
        if rank == seen:
            return r["0"]
            
    # maybe there were not enough names to get to as low a rank as requested, return empty string
    print("WARNING: Not enough names to get the rank requested")
    return ""

# takes a name, gender and birth year and determines what your name would be in a different year
# if it was the same ranked popular name for a given gender
def what_is_name_in_year(name: str, birth_year: int, new_year: int, gender: str)-> str:
    rank = get_rank(birth_year, name, gender)
    ret_val = get_name(new_year, rank, gender)

    return ret_val

def year_of_highest_rank(name: str, start_year: int, end_year: int, gender: str) -> int:
    best_rank = 10000000
    best_year = 0
    for y in range(start_year, end_year + 1):
        r = get_rank(y, name, gender)
        if r > 0 and r < best_rank:
            best_rank = r
            best_year = y
    
    return best_year

def avg_rank_for_range(name: str, start_year: int, end_year: int, gender: str) -> int:
    rank_total = 0
    for y in range(start_year, end_year + 1):
        r = get_rank(y, name, gender)
        if r > 0:
            rank_total += r
    
    return rank_total / (end_year - start_year + 1)

def births_ranked_higher(name: str, year: int, gender: str) -> int:
    if year < 1880 or year > 2014:
        print("No data available for this year.")
        return ""
    
    count = 0
    _cols, rows = read_csv_file("us_babynames/us_babynames_by_year/yob" + str(year) + ".csv", False)
    for r in rows:
        if gender != r["1"]:
            continue

        if r["0"] == name:
            return count
        
        count += int(r["2"])
    
    print("WARNING: Did not find name to find births more than, returning all births for given gender")
    return count
    
# total_births("us_babynames/us_babynames_test/example-small.csv")
print(str(get_rank(1971, "Frank", "M")))
# print(get_name(1975, 5, "M"))
# print(what_is_name_in_year("David", 1975, 2014, "M"))
# print(str(year_of_highest_rank("Mich", 1880, 2014, "M")))
# print(str(avg_rank_for_range("Susan", 1880, 2014, "F")))
# print(str(avg_rank_for_range("Robert", 1880, 2014, "M")))
#print(str(births_ranked_higher("Drew", 1990, "M")))

# total_births("us_babynames/us_babynames_by_year/yob1905.csv")

# print(what_is_name_in_year("Owen", 1974, 2014, "M"))

