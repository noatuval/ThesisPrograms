#serendipity formula computation 1 surprise1 = minimum weighted distance to rated items, surprise2 = average weighted distance to rated items with considering only cared features in user profile
import pandas as pd
import numpy as np
import pyodbc
import xlsxwriter
import sys
import math
import csv
import sys


min_user_number = int(input("* Enter from user_number: "))
max_user_number = int(input("* Enter to user_number+1: ")) 
#Input files

user_file = ['C:/bear/MovieLens Dataset/Serendipity Experiment/Alain Files thr05 with user and movie ID/CSV files/SerendipityMoviesDomainUser{:02d}.csv'.format(i) for i in range(min_user_number, max_user_number)]
profiles_file = 'C:/bear/MovieLens Dataset/Serendipity Experiment/serendipity formula/Profiles-ONE LINE PER A USER-02.csv'
effective_features_file = 'C:/bear/MovieLens Dataset/Serendipity Experiment/serendipity formula/USER PROFILES - EFFECTIVE FEATURES.csv'
weights_file = 'C:/bear/MovieLens Dataset/Serendipity Experiment/serendipity formula/AbsWeightsOneLine0-1 users1to444.csv'
#answers_file = ['C:/bear/MovieLens Dataset/Serendipity Experiment/Answers_sorted_new_with_results.csv']
#Results file
workbook_serendipity_formula_results = xlsxwriter.Workbook('C:/bear/MovieLens Dataset/Serendipity Experiment/serendipity formula/Weighted Distance to the rated items-23-05-23.xlsx')
worksheets_serendipity_formula_results = [workbook_serendipity_formula_results.add_worksheet() for i in range(1)]
worksheets_serendipity_formula_results[0].write(0, 0, 'User Num')
worksheets_serendipity_formula_results[0].write(0, 1, 'User Id')
worksheets_serendipity_formula_results[0].write(0, 2, 'Movie Id')
worksheets_serendipity_formula_results[0].write(0, 3, '#cared features')
worksheets_serendipity_formula_results[0].write(0, 4, 'minimum weighted distance')
worksheets_serendipity_formula_results[0].write(0, 5, 'minimum weighted distance/#features')
worksheets_serendipity_formula_results[0].write(0, 6, 'average weighted distance')
worksheets_serendipity_formula_results[0].write(0, 7, 'average weighted distance/#features')
with open(profiles_file, encoding='utf8', newline='') as csvfile:
        table_p = csv.reader(csvfile)
        dataset_profile = list(table_p)
with open(effective_features_file, encoding='utf8', newline='') as csvfile:
        table_e = csv.reader(csvfile)
        dataset_effective = list(table_e)
with open(weights_file, encoding='utf8', newline='') as csvfile:
        table_w = csv.reader(csvfile)
        dataset_weights = list(table_w)
line_profile = 0

output_line = 1
#with open(answers_file, encoding='latin1', newline='') as csvfile:
#    table_d = csv.reader(csvfile)
#    dataset_answers = list(table_d)
for user_num1 in range(min_user_number, max_user_number):
    user_num = user_num1 - min_user_number 

#    read_file = pd.read_csv (r'C:/bear/MovieLens Dataset/Serendipity Experiment/Alain Files thr05 with user and movie ID/TEMP TXT/SerendipityMoviesDomainUser' + str(user_indx) + '.txt', delimiter=' ',header=None)
#    read_file.to_csv (r'C:/bear/MovieLens Dataset/Serendipity Experiment/Alain Files thr05 with user and movie ID/CSV files/SerendipityMoviesDomainUser' + str(user_indx) + '.csv', sep = ',', index=None)    
#    user_file = 'C:/bear/MovieLens Dataset/Serendipity Experiment/Alain Files thr05 with user and movie ID/CSV files/SerendipityMoviesDomainUser' + str(user_indx) + '.csv'


    with open(user_file[user_num], encoding='utf8', newline='') as csvfile:
        table_d = csv.reader(csvfile)
        dataset_user = list(table_d)

        user_features = int(dataset_user[0][0])
        user_test_lines = int(dataset_user[0][1])
        user_training_lines = int(dataset_user[0][2])
        user_scale = int(dataset_user[0][3])
        user_id = dataset_user[0][4]
        print("user number=",user_num + 1,"user id=",user_id)
        

        #        line_answers = 1
#       userid_answers = dataset_answers[line_answers][0]
        line_user_test = 2
        while line_user_test <= user_test_lines + 1: 
            min_difference = user_features * 10
            sum_difference = 0
            
            line_user_training = user_test_lines + 2
           
            while line_user_training <= user_test_lines + user_training_lines + 1:
                column_user = 2
                feature_difference = 0
                while column_user <= user_features + 1:
                    
                    if int(dataset_profile[line_profile][column_user]) != 0:
                        
                        if dataset_user[line_user_training][column_user] != dataset_user[line_user_test][column_user]:
                            feature_difference += float(dataset_weights[line_profile][column_user])
                    column_user += 1
                sum_difference += feature_difference
                if feature_difference < min_difference:
                    min_difference = feature_difference
  #              print('test movie=',dataset_user[line_user_test][0],'training movie=',dataset_user[line_user_training][0],'difference=',feature_difference,'min_difference=',min_difference,'sum_difference=',sum_difference,'user_training_lines=',user_training_lines)
                line_user_training += 1
 #           print('min_difference=',min_difference,'sum_difference=',sum_difference,'user_training_lines=',user_training_lines,'actual_user_features=',int(dataset_effective[line_profile][2]))
            worksheets_serendipity_formula_results[0].write(output_line, 0, user_num + 1)
            worksheets_serendipity_formula_results[0].write(output_line, 1, user_id)
            worksheets_serendipity_formula_results[0].write(output_line, 2, dataset_user[line_user_test][0])
            worksheets_serendipity_formula_results[0].write(output_line, 3, dataset_effective[line_profile][2])
            worksheets_serendipity_formula_results[0].write(output_line, 4, min_difference)
            worksheets_serendipity_formula_results[0].write(output_line, 5, (min_difference / int(dataset_effective[line_profile][2])))
            worksheets_serendipity_formula_results[0].write(output_line, 6, sum_difference/user_training_lines)
            worksheets_serendipity_formula_results[0].write(output_line, 7, ((sum_difference/user_training_lines) / int(dataset_effective[line_profile][2])))

#     not right       worksheets_serendipity_formula_results[0].write(output_line, 3, user_scale - ((min_difference * (user_scale - 1)) / int(dataset_effective[line_profile][2])))
#     not right       worksheets_serendipity_formula_results[0].write(output_line, 4, user_scale -(((sum_difference/user_training_lines) * (user_scale - 1)) / int(dataset_effective[line_profile][2])))
            
            output_line += 1
            line_user_test += 1
        line_profile += 1
workbook_serendipity_formula_results.close()

                




