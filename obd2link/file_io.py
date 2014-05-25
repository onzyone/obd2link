import csv


#TODO add folder location
def write_csv(some_dict):

    with open('/tmp/mycsvfile.csv', 'wb') as f:  # Just use 'w' mode in 3.x
        w = csv.DictWriter(f, some_dict.keys())
        #TODO if there is a header append to the bottom of the file
        w.writeheader()
        w.writerow(some_dict)

def read_yaml():
    print 'will be used to read yaml config, logging etc files'

