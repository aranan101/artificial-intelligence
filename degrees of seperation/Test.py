from degrees import *
import os

## Load in raw data 
cwd = os.getcwd()

load_data(cwd +"/large")
print(shortest_path('kevin bacon', 'tom cruise'))
print(shortest_path('emma watson', 'jennifer lawrence'))
print(shortest_path('bruce lee', 'audrey hepburn'))