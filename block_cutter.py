# Block_Cutter
# By Patrick Vo and Jaspal Bainiwal
# Cuts the training dataset into chunks, with each chunk consisting of all records for 1/20th
#    of the items in the dataset

import pandas as pd
from sklearn.model_selection import train_test_split
from math import ceil

#Read in the full training data
train = pd.read_csv('train.csv')

#Find the unique names in the dataset and put them into a dataframe
names = train['item_nbr'].unique()
names = pd.DataFrame(names)

#Rename the names dataframe
names.columns = ['item_nbr']

#Find the length of 1/20 of the names dataset
length_of_name = ceil(len(names)/20)

# A for loop that goes through the training dataset 20 ids at a time,
#    cuts the data into blocks, then writes the blocks to csv
for i in range (1,20):
    
    #Define starting and ending lines for each line of code
    start_line = (i - 1) * length_of_name
    end_line = (i) * length_of_name
    
    #If the difference is too short (e.g. at the end of the file), then set end_line to the 
    #    last line in the file
    if ((end_line - start_line) < length_of_name):
        end_line = len(names) - 1
    
    # Find 20 names in the names dataset and merge with the training set. Rename index and drop the columns
    selected_names = names.iloc[start_line:end_line]
    selected_names['in_set'] = 1
    merged_items_and_records = pd.merge(train, selected_names, on = 'item_nbr')
    
    #Subset the new dataset based on the presence of the "in_set" variable
    csv_writer = merged_items_and_records[merged_items_and_records['in_set'] == 1]
    csv_writer.drop('in_set', axis = 1, inplace = True)
    csv_writer.reset_index(inplace = True)
    csv_writer.rename(columns = {'index': 'item_nbr'})
    
    #Take the resulting data and write to CSV
    csv_name = 'train' + str(i) + '.csv'
    csv_writer.to_csv(csv_name, sep = ',')