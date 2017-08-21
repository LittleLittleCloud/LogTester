import csv
def readCSV(file_path):
    res = []
    with open(file_path, 'r') as f:
        spamreader = csv.reader(f)
        for row in spamreader:
            if len(row) == 0:
                continue
            res.append(row)
    return res

