import csv


#TODO add folder location
def write_csv(some_dict):

    with open('/tmp/mycsvfile.csv', 'wb') as f:  # Just use 'w' mode in 3.x
        w = csv.DictWriter(f, some_dict.keys())
        w.writeheader()
        w.writerow(some_dict)