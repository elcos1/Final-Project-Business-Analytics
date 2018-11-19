import pandas as pd
import numpy as np
import json
import ast
from sklearn import preprocessing

def column_index(df, query_cols):
    cols = df.columns.values
    sidx = np.argsort(cols)
    return sidx[np.searchsorted(cols,query_cols,sorter=sidx)]

def main():
    path = r"C:\Users\Michal\Desktop\School\Bocconi\Courses\Business Analytics\FINAL\ted_main.csv"
    dataset = pd.read_csv(path)
    dataset.to_csv("ted_main.csv", encoding='utf-8', index=False)
    ratings = dataset['ratings']
    print(ratings[1])
    #dict_test = json.loads(ratings[1])
    #print(dict_test)
    my_distinct_list = [0]*40
    list_of_ratings = []
    flag = 0
    for j in range(len(ratings)):
        eval = ast.literal_eval(ratings[j])
        if len(eval) != 14:
            flag = 1
        for i in range(len(eval)):
            if my_distinct_list[eval[i].get('id')] == 0:
                my_distinct_list[eval[i].get('id')]+=1
                list_of_ratings.append(eval[i].get('name'))

        #print(len(list_of_ratings))
    #data_ratings = pd.DataFrame(eval)
    #print(data_ratings.head())

    print(type(eval))
    print(type(eval[1]))
    print(list_of_ratings)
    Series = pd.Series(0 for i in range(len(dataset)))
    for ratin_name in list_of_ratings:
        new_dataset = dataset.assign(temp=Series)
        name_list = list(new_dataset)
        name_list.pop()
        name_list.append(ratin_name)
        new_dataset.columns=name_list
        dataset = new_dataset
    print(list(new_dataset))
    print (flag)

    print(column_index(dataset, eval[1].get('name')))

    for j in range(len(ratings)):
        eval = ast.literal_eval(ratings[j])
        for i in range(len(eval)):
            name = eval[i].get('name')
            value = eval[i].get('count')
            dataset.iloc[j, column_index(dataset, name)] = int(value)

    # dataframe.at[row,col] = value
    #we have 14 ratings in total.
    
    # creating a list of column names to be standardized
    names = ['Funny', 'Beautiful', 'Ingenious', 'Courageous', 'Longwinded', 'Confusing', 'Informative', 'Fascinating', 'Unconvincing', 'Persuasive', 'Jaw-dropping', 'OK', 'Obnoxious', 'Inspiring']
    # standardizing the values of ratings columns
    std_scale = preprocessing.StandardScaler().fit(dataset[names])
    # assigning standardized values back to the dataset
    dataset[names] = std_scale.transform(dataset[names])
    
    # Loading LIWC data
    LIWC_data = pd.read_csv(r"C:\Users\Michal\Desktop\School\Bocconi\Courses\Business Analytics\FINAL\all_with_liwc_segmented.csv", header = 0, delimiter = ";")
    # defining columns to merge to previous dataset
    cols_to_use = LIWC_data.columns.difference(dataset.columns)
    # merging both datasets 
    merged_dataset = pd.merge(dataset, LIWC_data[cols_to_use], left_index=True, right_index=True, how='outer')
    
    
    #exporting csv
    print("saving the csv")
    merged_dataset.to_csv('dataset_with_ratings.csv',encoding='utf-8',index=False)
    print("csv saved")
    
main()