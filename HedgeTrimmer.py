# By Patrick Vo and Jaspal Bainiwal
import numpy as np
import pandas as pd
from random import random


#Read in the full training dataset from Corporacion Favorita
train = pd.read_csv('train.csv')


#Create a dataframe of unique item numbers from the training set.
item_numbers = train['item_nbr'].unique()
item_numbers = pd.DataFrame(item_numbers)


# For each unique item number, generate a random number between 0 and 1.
# Set a new column equal to 1 if the random number is less than 0.1
# This will cut the dataset into approximately 1/10th of the size, but will also include
#    every row for a certain item, allowing us to still explore time series trends
item_numbers['in_set'] = item_numbers[0].apply(lambda x: int(random() < 0.05))
item_numbers.columns = ['item_nbr', 'in_set']

# Create a new cut-down dataset by merging the training set and the item numbers,
#    then subsetting the training set by rows where item_nbr = 1
# Also delete train for space considerations
merged = pd.merge(train, item_numbers, on = ['item_nbr'])
del(train)
cut_down = merged[(merged['in_set'] == 1)]


#Reset the index, drop the inset variable, and rename the columns
cut_down = cut_down.drop('in_set', axis = 1)
cut_down.reset_index(inplace = True)
cut_down.rename(columns = {'index': 'id', 'id': 'transaction_id'}, inplace = True)

cut_down.to_csv('cut_down.csv', sep = ',')
