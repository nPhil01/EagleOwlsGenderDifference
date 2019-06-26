import os
import csv
import numpy as np

csvPath = "/Users/user/Desktop/eagle_owl/eagle_owl.csv"

with open(csvPath) as csvfile:
    data = np.array(list(csv.reader(csvfile, delimiter=",")))


reduced_data = data[:,[1,3,8,10,]]  #Drop all columns except for declared indices
reduced_data = np.delete(reduced_data,[4,18] ,axis=0, )  # Drop rows with empty fields

print(reduced_data[18])

