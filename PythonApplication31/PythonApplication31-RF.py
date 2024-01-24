# experiment04 - 200 users each time, Movie Domain, increasing training set, 10 test sets, 10 sets for user - RandomForest. Parameters: n_estimators = 100, random_state = 0
#All 200 (or  x) users in one run. Creating One worksheet per user + a file with the TOTAL Average Error across the 200 (or  x) users.
import pandas as pd
import numpy as np
from sklearn import linear_model
from sklearn import svm
from sklearn import tree
from sklearn.model_selection import PredefinedSplit
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor
from sklearn.naive_bayes import MultinomialNB
from sklearn.tree import DecisionTreeRegressor
from sklearn.neural_network import MLPRegressor
from sklearn.svm import LinearSVR
from sklearn.svm import SVR
import pyodbc
import xlsxwriter
import sys
import math
import csv


min_user_number = int(input("* Enter from user_number: "))
max_user_number = int(input("* Enter to user_number+1: ")) 
partial_training_set_size_max = int(input("* Enter partial training set size max: ")) 
training_set_size = 45
test_set_size = 5
number_of_test_sets = 10
number_of_tests_per_size = 10
#partial_training_set_size_max = 45


#user_num1 = int(input("* Enter user number: ")) 
#training_set_size = int(input("* Enter training-set size: "))
#test_set_size = int(input("* Enter test-set size: "))
#number_of_test_sets = int(input("* Enter number of test sets: "))
#number_of_tests_per_size = int(input("* Enter number of tests per size: "))
#partial_training_set_size_max = int(input("* Enter partial training-set size max: "))

testset_first_line = [1, 6, 11, 16, 21, 26, 31, 36, 41, 46]
#Random lines# of the training set
r_lines = [[21,23,9,24,15,39,22,10,8,13,2,41,35,25,45,44,12,32,19,29,16,42,46,26,49,4,27,6,18,43,38,20,50,5,28,11,30,17,36,33,7,37,48,31,14,40,34,3,47,1],
[41,40,16,34,22,14,8,33,26,9,15,29,3,31,2,4,44,38,49,20,39,6,42,45,30,7,43,24,25,47,46,5,1,32,23,21,12,17,37,13,36,18,19,11,35,28,50,27,10,48],
[20,22,14,24,5,43,17,35,44,27,25,21,11,28,48,45,9,49,10,2,38,29,39,15,13,23,18,6,12,47,1,4,34,26,7,41,37,19,16,32,42,36,3,30,46,50,33,31,8,40],
[19,45,33,3,14,39,16,42,41,5,38,9,27,32,28,12,24,11,37,23,6,26,50,34,43,7,15,31,25,30,40,13,46,49,10,35,2,44,8,17,36,21,18,20,22,1,4,29,48,47],
[16,1,40,3,34,32,18,33,23,39,46,38,7,21,17,14,41,5,49,28,44,22,11,25,9,30,31,43,13,42,6,26,2,19,29,20,12,15,27,48,36,10,4,50,8,47,37,35,45,24],
[49,26,3,31,45,4,41,8,23,18,1,30,28,9,50,7,38,34,11,29,44,14,21,37,22,42,25,48,13,17,46,10,12,36,20,47,24,15,16,5,39,6,33,27,2,19,32,43,35,40],
[23,7,39,43,45,44,9,26,15,48,46,32,3,14,31,50,16,25,10,18,11,13,6,5,22,30,41,36,24,2,47,17,42,8,4,37,29,38,40,20,34,35,27,12,1,21,33,49,19,28],
[10,4,36,45,38,41,11,39,28,30,15,5,48,20,18,21,16,47,37,32,23,40,9,50,2,26,13,8,22,34,19,17,12,42,7,31,24,49,25,6,33,44,46,43,35,1,27,3,29,14],
[47,33,4,50,35,28,43,20,6,42,45,17,30,22,44,38,48,8,29,7,36,16,26,27,39,10,18,2,41,32,3,14,23,37,40,1,25,34,46,24,11,5,31,12,19,49,15,13,21,9],
[8,34,16,28,14,31,13,39,27,20,15,45,23,12,4,6,44,29,35,19,50,18,46,42,36,41,5,33,37,11,1,26,22,38,7,24,49,10,9,21,32,2,40,30,3,43,48,47,17,25]]
user_file = ['C:/bear/MovieLens Dataset/Data files-EXPERIMENT04/EXPERIMENT04-all users/Noa files/CSV files/MoviesDomainUser{:02d}.csv'.format(i) for i in range(min_user_number, max_user_number)]
#user_file = 'C:/bear/MovieLens Dataset/Data files-EXPERIMENT04/CSV Datasets - EXPERIMENT04/MoviesDomainUser01.csv'
#Users 1-200:
#number_of_features_per_user = [753,696,735,748,627,649,745,712,796,755,667,718,726,744,727,768,710,773,754,700,727,767,721,758,768,784,764,706,668,766,691,767,743,762,784,734,765,688,758,772,755,736,734,757,776,702,747,720,776,557,747,746,771,719,600,742,781,700,593,778,707,769,754,725,730,726,683,737,741,764,774,768,708,733,749,793,729,779,702,763,717,710,760,745,717,744,750,775,728,785,778,793,771,756,770,754,738,634,776,769,762,767,733,704,719,753,683,733,768,708,717,785,765,766,751,748,637,725,722,704,779,743,782,703,640,740,690,762,739,745,782,717,654,701,716,761,704,770,771,772,746,763,716,710,750,704,749,720,687,701,682,736,786,785,744,754,735,735,775,752,696,788,717,782,574,704,733,705,729,758,681,726,764,736,735,790,771,654,710,777,803,704,680,739,745,789,766,674,713,727,689,786,752,711,791,591,744,789,702,755]
#Users 201-400:
#number_of_features_per_user = [710,629,758,752,724,712,723,716,643,709,696,705,755,774,675,722,776,770,756,793,772,769,742,794,716,743,780,757,707,660,761,683,684,625,735,681,761,768,765,754,771,744,619,772,793,633,730,726,777,762,754,705,764,729,764,798,747,725,688,762,697,757,748,780,753,741,630,742,796,730,762,759,761,741,630,668,693,793,708,785,737,780,758,742,758,717,738,743,710,733,710,736,751,757,702,754,777,769,770,702,745,737,775,682,764,794,726,783,678,791,704,774,768,757,756,674,668,734,652,734,736,710,757,739,752,756,764,808,738,795,784,772,768,740,758,771,777,743,762,776,718,756,440,664,767,718,756,786,779,774,758,798,748,748,694,721,792,761,694,789,731,696,699,632,716,620,662,776,706,594,786,755,750,783,798,703,747,759,752,772,686,770,758,733,714,764,787,717,730,655,792,780,628,773,746,768,689,759,749,766]
#Users 401-600:
#number_of_features_per_user = [762,701,701,760,529,734,751,765,706,726,751,726,751,748,732,721,712,759,724,763,739,734,709,756,741,685,758,740,704,734,752,750,737,752,710,723,796,683,769,756,722,791,754,792,738,714,693,708,730,737,791,733,780,709,776,663,752,719,780,745,747,694,718,691,593,746,726,702,766,741,791,796,807,746,758,704,763,775,719,780,742,640,765,714,670,707,794,760,684,763,730,680,760,717,732,702,697,728,731,697,734,715,783,772,713,739,664,764,719,683,756,724,619,791,769,784,716,740,729,650,755,750,784,736,722,773,706,665,720,825,783,754,739,735,743,756,807,758,758,800,738,724,770,741,678,761,668,748,720,703,784,739,758,761,784,762,757,751,787,733,722,700,601,655,711,743,744,769,781,600,763,749,765,724,677,687,763,766,743,770,752,726,778,681,733,684,723,779,634,765,677,779,772,753,755,749,697,676,767,755]
#Users 601-800:
#number_of_features_per_user = [758,706,706,744,766,720,676,605,726,780,701,777,788,768,715,730,727,757,755,772,741,733,678,635,756,715,634,788,765,788,775,747,784,787,682,789,471,708,771,807,787,766,764,467,734,706,755,673,729,703,748,751,759,763,766,682,763,735,711,712,776,746,671,693,729,695,756,695,781,762,785,769,703,708,771,757,761,752,732,696,756,639,767,790,755,736,728,723,760,793,760,748,765,783,741,779,705,758,693,720,744,695,674,719,777,766,724,783,717,752,677,730,760,803,751,740,804,691,715,770,700,775,697,728,709,759,683,776,757,733,815,669,727,776,734,762,741,768,728,741,687,786,727,731,748,769,830,793,767,745,744,758,777,664,724,755,724,692,684,772,785,685,727,681,755,688,740,690,814,772,792,724,785,744,756,762,758,657,691,764,786,725,727,752,761,789,661,717,741,793,751,620,809,741,723,760,794,764,696,635]
#Users 801-1000:
number_of_features_per_user = [770,723,755,745,728,772,746,750,705,683,796,787,768,707,752,712,844,725,791,800,768,735,788,768,766,781,740,727,683,680,739,735,731,764,616,679,672,741,754,765,717,525,768,733,741,721,668,778,764,720,772,709,749,693,647,729,782,764,786,792,755,734,740,777,665,763,763,695,722,807,744,616,722,727,729,760,557,664,711,752,758,690,751,763,771,746,779,764,783,719,773,719,796,758,766,701,780,686,805,749,769,765,727,764,719,594,750,754,595,745,782,734,757,733,744,687,714,755,754,576,746,719,723,712,808,761,728,747,746,743,719,713,724,762,768,755,752,649,777,759,763,797,788,742,717,713,768,664,764,735,760,755,738,742,758,752,783,770,753,744,778,741,721,712,730,742,722,798,751,758,725,681,763,778,712,624,741,774,797,804,764,735,768,768,455,757,793,682,776,754,766,753,659,695,760,690,775,783,768,751]
workbook_totals = xlsxwriter.Workbook('C:/bear/MovieLens Dataset/Data files-EXPERIMENT04/EXPERIMENT04-all users/Results-project31 tests/RandomForestMoviesDomain/RFusers ' + str(min_user_number) + '-' + str(max_user_number - 1) + ' Totals-n.xlsx')
worksheets_totals = [workbook_totals.add_worksheet() for i in range(1)]
worksheets_totals[0].write(0, 0, "Size of the training set")
    

for user_num1 in range(min_user_number, max_user_number):
    #Results file
    workbook = xlsxwriter.Workbook('C:/bear/MovieLens Dataset/Data files-EXPERIMENT04/EXPERIMENT04-all users/Results-project31 tests/RandomForestMoviesDomain/RFMoviesDomainUser' + str(user_num1) + '-n.xlsx')

    worksheets = [workbook.add_worksheet() for i in range(number_of_test_sets + 1)]
    worksheets[number_of_test_sets].write(0, 0, "Size of the training set")
    worksheets[number_of_test_sets].write(0, 1, "RF Average error 10 test sets")
    worksheets_totals[0].write(0, user_num1 - min_user_number + 1, "RF Av. error user "+str(user_num1))

    user_num = user_num1 - min_user_number
 #   print('user_num = ',user_num)
    #starting from L=1
    partial_training_set_size = 0

    while partial_training_set_size < partial_training_set_size_max:
    
    #    average_prediction_error_per_user = 0
        average_prediction_error_per_testset = 0
        partial_training_set_size += 1
    #    while user_num < number_of_users: 

        print('partial_training_set_size=',partial_training_set_size)
        testset_number = 0
        while testset_number < number_of_test_sets:
            worksheets[testset_number].write(0, 0, "Size of the training set")
            worksheets[testset_number].write(0, 1, "RF Average error for 10 tests per a test set")
            worksheets[testset_number].write(0, 2, "RF Average error for test 1")
            worksheets[testset_number].write(0, 3, "RF Average error for test 2")
            worksheets[testset_number].write(0, 4, "RF Average error for test 3")
            worksheets[testset_number].write(0, 5, "RF Average error for test 4")
            worksheets[testset_number].write(0, 6, "RF Average error for test 5")   
            worksheets[testset_number].write(0, 7, "RF Average error for test 6")
            worksheets[testset_number].write(0, 8, "RF Average error for test 7")
            worksheets[testset_number].write(0, 9, "RF Average error for test 8")
            worksheets[testset_number].write(0, 10, "RF Average error for test 9")
            worksheets[testset_number].write(0, 11, "RF Average error for test 10")
            print('testset_number=',testset_number)
    #Creating the test-set file
            with open(user_file[user_num], encoding='utf8', newline='') as csvfile:
    #        with open(user_file, encoding='utf8', newline='') as csvfile:
                print('user_file[user_num]=',user_file[user_num])
                table_d = csv.reader(csvfile)
                table_data = list(table_d)
            with open('C:/bear/MovieLens Dataset/Data files-EXPERIMENT04/CSV Datasets - EXPERIMENT04/Results-project31 tests/EXPERIMENT04 Scikit-Test set.csv', 'w', newline='') as f_test:
                writer = csv.writer(f_test)
                writer.writerow(table_data[(testset_number * test_set_size) + 1])
            with open('C:/bear/MovieLens Dataset/Data files-EXPERIMENT04/CSV Datasets - EXPERIMENT04/Results-project31 tests/EXPERIMENT04 Scikit-Test set.csv', 'a', newline='') as f_test:
                writer = csv.writer(f_test)
                for i in range(2, test_set_size + 1):
                    writer.writerow(table_data[(testset_number * test_set_size) + i])
            f_test.close
            with open('C:/bear/MovieLens Dataset/Data files-EXPERIMENT04/CSV Datasets - EXPERIMENT04/Results-project31 tests/EXPERIMENT04 Scikit-Test set.csv', encoding='utf8', newline='') as csvfile:
                table_t = csv.reader(csvfile)
                table_test = list(table_t)
            set_num = 0
            average_prediction_error_per_set = 0
            output_column_position = 1
            while set_num < number_of_tests_per_size:
    #               print('set_num=',set_num)
    #Creating the input file
                
                with open('C:/bear/MovieLens Dataset/Data files-EXPERIMENT04/CSV Datasets - EXPERIMENT04/Results-project31 tests/EXPERIMENT04 Scikit-var Test set and var Training set.csv', 'w', newline='') as f_test:
                    writer = csv.writer(f_test)
                    writer.writerow(table_data[0])

                l_num = 0
                while l_num < test_set_size:
                    with open('C:/bear/MovieLens Dataset/Data files-EXPERIMENT04/CSV Datasets - EXPERIMENT04/Results-project31 tests/EXPERIMENT04 Scikit-var Test set and var Training set.csv', 'a', newline='') as f_test:
                        writer = csv.writer(f_test)
                        writer.writerow(table_test[l_num])
                    l_num += 1
                f_test.close

                     
    # Lines of the input file
                items_num = 0
                dlta = 0
                line_position = 1
                while items_num < partial_training_set_size:
                                
                    with open('C:/bear/MovieLens Dataset/Data files-EXPERIMENT04/CSV Datasets - EXPERIMENT04/Results-project31 tests/EXPERIMENT04 Scikit-var Test set and var Training set.csv', 'a', newline='') as f:
    #                      print('items_num=', items_num)
                        while (r_lines[set_num][items_num + dlta] >= testset_first_line[testset_number]) and (r_lines[set_num][items_num + dlta] < testset_first_line[testset_number] + test_set_size):
                            dlta += 1
                            #print('*items_num=', items_num,'dlta=',dlta,'r_lines[set_num][items_num + dlta]=',r_lines[set_num][items_num + dlta])
                        writer = csv.writer(f)
                        writer.writerow(table_data[r_lines[set_num][items_num + dlta]])
                        #print('**items_num=', items_num,'dlta=',dlta,'r_lines[set_num][items_num + dlta]=',r_lines[set_num][items_num + dlta])
                        #print(table_data[r_lines[set_num][items_num + dlta]])
                        items_num += 1
                    line_position +=1                             
                f.close()

                dataset = pd.read_csv('C:/bear/MovieLens Dataset/Data files-EXPERIMENT04/CSV Datasets - EXPERIMENT04/Results-project31 tests/EXPERIMENT04 Scikit-var Test set and var Training set.csv')
                x = dataset.iloc[:, 0:number_of_features_per_user[user_num]].values
                y = dataset.iloc[:, number_of_features_per_user[user_num]].values
                
                sheet_num = 0
    # Train on the samples 5 to the end, test on the first 5 samples.
    #[5] specifies the index at which the array is splitted.
                x_test, x_train = np.array_split(x, [5])
                y_test, y_train = np.array_split(y, [5])

                clf = RandomForestRegressor(n_estimators = 100, random_state = 0)
                y_pred = clf.fit(x_train, y_train).predict(x_test)

                average_prediction_error = 0
                sum_of_prediction_errors = 0
        
        
                for i in range(0, test_set_size): 
                    sum_of_prediction_errors += abs(y_test[i] - round(y_pred[i],0))
       
                average_prediction_error = sum_of_prediction_errors / test_set_size
                average_prediction_error_per_set = average_prediction_error_per_set + average_prediction_error
                output_column_position +=1
                worksheets[testset_number].write(partial_training_set_size, output_column_position, average_prediction_error)

                set_num += 1
#                print('set_num=',set_num)

            worksheets[testset_number].write(partial_training_set_size, 0, partial_training_set_size)
            average_prediction_error_per_set = average_prediction_error_per_set / number_of_tests_per_size
            worksheets[testset_number].write(partial_training_set_size, 1, average_prediction_error_per_set)
            average_prediction_error_per_testset += average_prediction_error_per_set
            testset_number += 1
    #        print('testset_number=',testset_number)
    #            user_num += 1
        worksheets[testset_number].write(partial_training_set_size, 0, partial_training_set_size)
        worksheets[testset_number].write(partial_training_set_size, 1, average_prediction_error_per_testset / number_of_test_sets)
        worksheets_totals[0].write(partial_training_set_size, 0, partial_training_set_size)
        worksheets_totals[0].write(partial_training_set_size, user_num + 1, average_prediction_error_per_testset / number_of_test_sets)
        print('user=',user_num,'number_of_features_per_user[user_num]=',number_of_features_per_user[user_num])
    workbook.close()
workbook_totals.close()


