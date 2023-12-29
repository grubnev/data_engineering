import json
import pandas as pd
import matplotlib
import numpy as np
import os

pd.set_option("display.max_rows", 20, "display.max_columns", 60)

def read_file(file_name):
    return pd.read_csv(file_name)
    #df = pd.read_csv(file_name, chunksize=500_000, compression='zip')



file_name = "data/[1]game_logs.csv"
dataset = read_file(file_name)
file_size = os.path.getsize(file_name)