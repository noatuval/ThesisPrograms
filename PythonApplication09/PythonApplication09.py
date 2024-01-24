#Classifying  10 Users' data, Training set size=450, Test set size=50, using Cross validation 10 folds technique, Classifiers: SVM, Decision tree, Neural network, Naive Bayes, Random forest
#Functions and parameters are similar to those of project15 programs
import pyodbc
import xlsxwriter
import sys
import pandas as pd
import numpy as np
from sklearn import linear_model
from sklearn import svm
from sklearn import tree
from sklearn.neural_network import MLPRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.model_selection import PredefinedSplit
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import SVR
import math
import csv

number_of_users = int(input("* Enter number of users: "))
training_set_size = int(input("* Enter training-set size: "))
test_set_size = int(input("* Enter test-set size: "))
number_of_tests_per_user = int(input("* Enter number of tests per user: "))
classification_methods = int(input("* Enter number of classification methods: "))

number_of_features_per_user = [49, 50, 50, 48, 51, 48, 50, 50, 49, 45]
#learning_set_line = int(1)
#test_set_line = int(training_set_line + learning_set_size + 1)
user_file = ['C:/bear/EXPERIMENT03 - User01 - CLS.csv', 'C:/bear/EXPERIMENT03 - User02 - CLS.csv', 'C:/bear/EXPERIMENT03 - User03 - CLS.csv', 'C:/bear/EXPERIMENT03 - User04 - CLS.csv', 'C:/bear/EXPERIMENT03 - User05 - CLS.csv', 'C:/bear/EXPERIMENT03 - User06 - CLS.csv', 'C:/bear/EXPERIMENT03 - User07 - CLS.csv', 'C:/bear/EXPERIMENT03 - User08 - CLS.csv', 'C:/bear/EXPERIMENT03 - User09 - CLS.csv', 'C:/bear/EXPERIMENT03 - User10 - CLS.csv']
methods_table = ['Svm', 'Decision Tree', 'Neural Network', 'NaiveBayes', 'RandomForest']
average_error_all_users_SVM = 0
average_error_all_users_DecisionTree = 0
average_error_all_users_NeuralNetwork = 0
average_error_all_users_NaiveBayes = 0
average_error_all_users_RandomForest = 0

#Results files
workbook = xlsxwriter.Workbook('C:/bear/Tests/ScikitRegressors Results-10Users-18-05-21B.xlsx')
worksheets = [workbook.add_worksheet() for i in range(1)]
worksheets[0].write(0, 0, "User#")
worksheets[0].write(0, 1, "Method")
worksheets[0].write(0, 2, "Average error")
worksheets[0].write(0, 3, "Average error for test 1")
worksheets[0].write(0, 4, "Average error for test 2")
worksheets[0].write(0, 5, "Average error for test 3")
worksheets[0].write(0, 6, "Average error for test 4")
worksheets[0].write(0, 7, "Average error for test 5")
worksheets[0].write(0, 8, "Average error for test 6")
worksheets[0].write(0, 9, "Average error for test 7")
worksheets[0].write(0, 10, "Average error for test 8")
worksheets[0].write(0, 11, "Average error for test 9")
worksheets[0].write(0, 12, "Average error for test 10")


#Reading the input csv file per user and Partitioning the dataset for the cross validation process 
user_num = 0

while user_num < number_of_users: 
    average_error_per_user_SVM = 0
    average_error_per_user_DecisionTree = 0
    average_error_per_user_NeuralNetwork = 0
    average_error_per_user_NaiveBayes = 0
    average_error_per_user_RandomForest = 0
    worksheets[0].write((user_num * classification_methods) + 1, 0, user_num + 1)
    with open(user_file[user_num], encoding='utf8', newline='') as csvfile:
        table_d = csv.reader(csvfile)
        table_data = list(table_d)
    set_num = 0
    average_prediction_error_per_set = 0
    output_column_position = 1
    while set_num < number_of_tests_per_user:
        set_num +=1
#Writing the attributes line
        print("set num = ",set_num)
        with open('C:/bear/EXPERIMENT03-Python17-05-21-CLS input file.csv', 'w', newline='') as fcls_file:
            writer = csv.writer(fcls_file)
            writer.writerow(table_data[0])
        fcls_file.close

#Writing the test set lines
        l0_num = (set_num - 1) * test_set_size + 1
        while l0_num < set_num  * test_set_size + 1:
            with open('C:/bear/EXPERIMENT03-Python17-05-21-CLS input file.csv', 'a', newline='') as fcls0_file1:
                writer = csv.writer(fcls0_file1)
                writer.writerow(table_data[l0_num])
                l0_num += 1
            fcls0_file1.close
#Writing the training set lines
        l_num = 0
        while l_num < training_set_size + test_set_size:
            l_num += 1
            if ((l_num < ((set_num - 1) * test_set_size + 1)) or (l_num > set_num  * test_set_size )):
                with open('C:/bear/EXPERIMENT03-Python17-05-21-CLS input file.csv', 'a', newline='') as fcls_file1:
                    writer = csv.writer(fcls_file1)
                    writer.writerow(table_data[l_num])
 #                   print(table_data[l_num])
                fcls_file1.close
        
        
        dataset = pd.read_csv('C:/bear/EXPERIMENT03-Python17-05-21-CLS input file.csv')
        x = dataset.iloc[:, 0:number_of_features_per_user[user_num]].values
        y = dataset.iloc[:, number_of_features_per_user[user_num]].values

# Classifing data using various classification methods
        sheet_num = 0
# Train on the samples 50 to the end, test on the first 50 samples.
#[test_set_size] specifies the index at which the array is splitted.
        x_test, x_train = np.array_split(x, [test_set_size])
        y_test, y_train = np.array_split(y, [test_set_size])
        c_method = 0
        while c_method < classification_methods: 
            if c_method == 0:
                clf = SVR(kernel='rbf', C=1, gamma=0.1, epsilon=.1)
          
            elif c_method == 1:
                clf = DecisionTreeRegressor(max_depth=100, random_state=0)

            elif c_method == 2:
                clf = MLPRegressor(random_state=0, max_iter=500,solver='lbfgs', alpha=1e-5, hidden_layer_sizes=(5, 2))

            elif c_method == 3:
                clf = MultinomialNB()

            elif c_method == 4:
                scl = StandardScaler()
                x_train = scl.fit_transform(x_train)
                x_test = scl.transform(x_test)                              
                clf = RandomForestRegressor(n_estimators = 100, random_state = 0)
            clf.fit(x_train, y_train)
            y_pred = clf.predict(x_test)
                       
            average_prediction_error = 0
            sum_of_prediction_errors = 0        
        
            work_col = 0
            for i in range(0, test_set_size): 
                sum_of_prediction_errors += abs(y_test[i] - round(y_pred[i],0))
                worksheets[sheet_num].write((user_num * classification_methods) + 1 + c_method, (set_num - 1) * 50 + work_col + 13, abs(y_test[i] - round(y_pred[i],0)))
                work_col += 1

            average_prediction_error = sum_of_prediction_errors / test_set_size
            
            if c_method == 0:
                average_error_per_user_SVM += average_prediction_error            
            elif c_method == 1:
                average_error_per_user_DecisionTree += average_prediction_error
            elif c_method == 2:
                average_error_per_user_NeuralNetwork += average_prediction_error
            elif c_method == 3:              
                average_error_per_user_NaiveBayes += average_prediction_error
            elif c_method == 4:              
                average_error_per_user_RandomForest += average_prediction_error
            worksheets[sheet_num].write((user_num * classification_methods) + 1 + c_method, set_num + 2, average_prediction_error)
            c_method += 1


    worksheets[sheet_num].write((user_num * classification_methods) + 1, 2, average_error_per_user_SVM / number_of_tests_per_user)
    worksheets[sheet_num].write((user_num * classification_methods) + 2, 2, average_error_per_user_DecisionTree / number_of_tests_per_user)
    worksheets[sheet_num].write((user_num * classification_methods) + 3, 2, average_error_per_user_NeuralNetwork / number_of_tests_per_user)
    worksheets[sheet_num].write((user_num * classification_methods) + 4, 2, average_error_per_user_NaiveBayes / number_of_tests_per_user)
    worksheets[sheet_num].write((user_num * classification_methods) + 5, 2, average_error_per_user_RandomForest / number_of_tests_per_user)
    worksheets[sheet_num].write((user_num * classification_methods) + 1, 1, "SVM")
    worksheets[sheet_num].write((user_num * classification_methods) + 2, 1, "Decision Tree")
    worksheets[sheet_num].write((user_num * classification_methods) + 3, 1, "Neural Network")
    worksheets[sheet_num].write((user_num * classification_methods) + 4, 1, "Naive Bayes")
    worksheets[sheet_num].write((user_num * classification_methods) + 5, 1, "Random Forest")
    average_error_all_users_SVM += (average_error_per_user_SVM / number_of_tests_per_user)
    average_error_all_users_DecisionTree += (average_error_per_user_DecisionTree / number_of_tests_per_user)
    average_error_all_users_NeuralNetwork += (average_error_per_user_NeuralNetwork / number_of_tests_per_user)
    average_error_all_users_NaiveBayes += (average_error_per_user_NaiveBayes / number_of_tests_per_user)
    average_error_all_users_RandomForest += (average_error_per_user_RandomForest / number_of_tests_per_user)
    user_num += 1

worksheets[sheet_num].write((user_num * classification_methods) + 2, 0, "Average error all users SVM: ")
worksheets[sheet_num].write((user_num * classification_methods) + 3, 0, "Average error all users Decision Tree: ")
worksheets[sheet_num].write((user_num * classification_methods) + 4, 0, "Average error all users Neural Network: ")
worksheets[sheet_num].write((user_num * classification_methods) + 5, 0, "Average error all users Naive Bayes: ")
worksheets[sheet_num].write((user_num * classification_methods) + 6, 0, "Average error all users Random Forest: ")
worksheets[sheet_num].write((user_num * classification_methods) + 2, 1, average_error_all_users_SVM / number_of_users )
worksheets[sheet_num].write((user_num * classification_methods) + 3, 1, average_error_all_users_DecisionTree / number_of_users)
worksheets[sheet_num].write((user_num * classification_methods) + 4, 1, average_error_all_users_NeuralNetwork / number_of_users)
worksheets[sheet_num].write((user_num * classification_methods) + 5, 1, average_error_all_users_NaiveBayes / number_of_users)
worksheets[sheet_num].write((user_num * classification_methods) + 6, 1, average_error_all_users_RandomForest / number_of_users)

workbook.close()
                    



