# experiment03 - 10 users, increasing training set, fixed test set, 10 sets for user - RandomForest. Parameters: n_estimators = 100, random_state = 0
import pandas as pd
import numpy as np
from sklearn import linear_model
from sklearn import svm
from sklearn import tree
from sklearn.model_selection import PredefinedSplit
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor 
import pyodbc
import xlsxwriter
import sys
import math
import csv

number_of_users = int(input("* Enter number of users: ")) 
training_set_size = int(input("* Enter training-set size: "))
partial_training_set_size_max = int(input("* Enter partial training-set size max: "))
test_set_size = int(input("* Enter test-set size: "))
number_of_tests_per_size = int(input("* Enter number of tests per size: "))

#Random lines# of the training set
r_lines = [[434,287,28,116,294,386,137,193,250,272,213,428,141,260,114,77,241,127,323,138,162,369,268,430,333,81,63,374,218,236,330,253,73,409,420,418,344,107,212,143,431,424,172,120,285,338,249,75,66,121,264,227,92,82,207,425,214,321,347,32,106,226,286,178,237,306,197,130,14,408,325,46,433,47,165,269,435,15,394,51,188,259,277,279,339,85,304,102,405,200,133,61,27,19,290,263,377,37,445,390,48,371,436,29,18,202,348,3,270,343,53,57,152,381,387,93,16,240,245,421,41,432,83,68,448,372,382,426,10,429,419,108,349,4,187,366,257,84,422,76,30,22,183,180,5,122,271,20,359,67,42,400,97,174,69,146,147,52,123,156,31,89,315,437,94,54,345,401,135,365,25,215,438,208,395,442,378,266,11,288,383,103,289,33,276,410,175,423,9,296,181,38,439,44,70,129,95,412,79,280,327,155,45,314,414,39,357,341,305,427,229,291,71,118,318,397,78,96,440,86,441,150,173,443,246,242,157,391,255,292,220,184,43,316,98,58,406,6,399,312,444,230,151,99,350,72,49,23,163,12,109,153,216,331,179,7,124,388,396,446,223,217,159,317,134,309,375,88,313,376,1,337,154,158,447,101,219,74,125,449,87,281,136,346,161,364,351,282,300,352,310,126,164,21,450,297,328,417,2,243,342,8,128,50,189,160,196,13,231,319,17,363,149,176,311,320,90,261,194,24,166,55,167,373,131,206,273,56,177,256,293,62,295,26,168,80,228,353,91,59,274,132,34,35,298,332,334,36,144,100,40,354,182,139,275,355,356,104,402,115,403,299,185,301,360,384,370,140,283,60,195,169,186,278,142,64,170,65,105,302,190,110,198,358,222,111,258,171,221,262,284,191,112,113,117,119,145,148,199,322,192,201,203,265,267,204,340,411,254,404,307,205,209,210,392,211,224,247,379,225,232,248,233,234,303,235,308,324,238,239,244,326,251,252,329,361,335,336,362,367,368,380,385,389,393,398,407,413,415,416],
           [107,153,45,298,350,344,90,154,229,304,201,432,198,289,260,402,186,285,440,93,166,28,355,30,50,265,336,380,444,386,178,101,89,222,450,40,168,91,193,396,445,446,430,191,283,291,142,70,177,183,162,343,211,118,424,312,382,310,241,376,297,418,78,385,242,77,425,408,165,219,406,159,213,437,401,97,277,145,167,3,379,381,397,192,48,371,52,31,282,345,8,128,363,137,115,206,214,141,163,431,411,170,190,225,156,194,321,34,388,92,94,317,71,35,57,119,7,161,200,288,106,261,18,19,398,184,224,160,324,438,195,284,158,383,58,365,172,433,1,110,69,95,426,139,175,84,308,182,244,109,72,351,368,140,420,314,323,245,74,248,232,263,133,441,243,246,409,16,223,410,125,342,98,152,82,272,290,442,55,81,99,126,32,17,318,53,384,196,299,5,39,131,319,173,121,164,413,130,179,236,87,356,127,185,108,262,59,395,250,112,79,403,237,169,20,157,215,400,346,113,6,435,247,377,171,415,143,120,96,369,407,233,273,83,21,387,394,75,378,197,187,4,144,25,174,216,180,389,176,129,41,220,111,333,146,320,300,337,38,443,254,447,226,132,76,249,114,22,370,37,264,181,42,9,188,205,227,412,189,436,147,274,207,302,199,404,202,54,286,208,46,100,203,322,218,327,204,328,399,85,416,212,238,10,271,23,266,43,33,47,80,209,325,287,24,86,235,210,217,123,449,281,267,221,151,36,88,315,414,73,448,375,292,293,434,155,305,251,252,338,294,329,116,228,230,231,347,2,374,102,234,373,357,439,239,117,26,301,422,27,372,419,405,255,256,390,417,240,253,257,103,122,104,259,391,303,11,278,349,366,421,105,340,360,60,61,29,134,423,44,258,330,62,268,135,367,148,124,136,392,348,269,49,12,51,427,332,138,306,270,13,307,309,393,275,358,56,295,63,14,326,276,334,15,428,66,352,149,279,64,65,67,311,150,280,429,296,68,313,316,331,335,339,341,353,354,359,361,362,364],
           [133,333,322,67,314,311,134,262,386,287,336,431,391,184,115,77,167,221,43,226,229,290,276,91,387,361,219,444,438,179,135,172,61,56,239,426,366,371,238,354,259,123,334,251,358,448,328,127,270,422,352,100,261,230,190,249,139,11,294,178,241,427,350,353,32,138,329,450,58,168,355,368,342,236,169,250,285,46,428,156,17,330,255,331,159,445,180,298,57,23,25,296,51,429,198,136,113,128,137,222,295,35,140,185,323,360,36,208,405,12,363,24,392,170,403,101,213,183,1,268,205,26,166,307,52,415,441,164,92,124,439,440,210,181,173,81,88,207,341,42,271,253,116,212,420,68,312,234,302,364,53,59,442,269,416,40,233,406,256,376,130,242,365,339,421,141,21,60,395,362,150,215,216,265,430,237,384,340,20,240,254,122,344,243,390,367,332,224,315,142,149,47,378,114,385,399,252,6,7,194,419,209,13,186,74,437,22,62,379,41,346,232,162,291,75,102,201,407,377,65,143,76,110,70,244,95,71,39,152,129,284,120,335,297,356,408,337,380,69,313,18,413,93,182,257,220,338,3,225,258,119,369,388,228,38,174,374,108,263,78,235,148,247,171,443,204,177,375,187,245,246,199,206,381,432,63,151,316,64,425,175,188,343,103,14,433,327,389,144,191,9,382,345,308,145,383,66,321,306,248,117,94,446,372,27,418,434,223,347,96,196,50,275,146,211,348,121,147,272,317,324,349,260,264,189,435,195,300,301,104,90,15,193,131,447,266,153,417,37,82,112,286,192,449,423,393,325,154,72,155,5,2,79,292,310,318,273,54,163,176,157,305,197,400,436,200,217,202,203,304,320,351,158,55,357,165,4,214,309,111,409,370,160,30,267,19,359,73,125,80,299,373,412,83,279,8,303,97,218,44,401,84,10,87,105,394,274,161,89,227,319,98,85,16,126,326,31,86,28,231,277,288,99,278,424,396,132,280,106,397,398,29,33,402,107,281,282,404,410,411,109,283,34,289,293,414,45,48,49,118],
           [28,17,79,163,151,47,75,334,314,187,250,221,195,269,116,342,443,390,288,364,299,441,90,353,264,332,80,408,155,372,147,234,389,226,396,141,272,73,77,135,259,326,407,3,196,74,397,240,12,235,154,362,276,243,317,91,125,395,48,331,368,245,114,358,20,111,101,343,183,177,81,442,104,36,46,300,108,444,88,171,277,241,136,102,34,1,244,210,447,341,92,365,137,255,324,207,366,424,152,150,202,231,140,305,266,237,153,426,280,292,198,158,138,333,312,220,335,105,429,328,445,120,294,182,374,219,388,340,246,89,39,446,371,232,301,188,69,53,214,349,398,411,56,82,293,367,302,227,76,329,106,67,448,449,248,423,217,238,313,10,378,351,4,298,184,354,86,252,8,303,156,5,315,257,85,157,228,435,379,304,316,84,416,311,83,265,336,306,51,199,359,30,159,414,380,385,318,15,186,376,369,387,381,229,193,68,382,21,103,360,319,417,49,337,330,127,148,215,27,251,13,437,281,216,401,209,149,267,278,338,247,191,321,230,19,117,345,450,139,2,361,54,413,404,391,344,133,87,160,211,339,170,197,218,436,161,425,134,16,307,70,320,94,392,93,112,55,432,113,239,31,71,295,44,25,233,386,212,322,95,22,200,323,222,412,352,418,438,96,33,346,162,347,434,142,431,97,249,14,205,35,98,279,325,143,355,107,78,164,18,223,185,268,144,6,282,99,415,270,172,7,208,373,393,192,62,427,348,363,439,145,394,100,23,327,273,375,24,399,146,37,165,370,308,356,377,126,440,384,9,213,433,253,130,383,11,254,350,400,166,402,109,167,72,110,26,357,115,118,287,256,168,57,173,29,32,119,189,38,40,236,201,58,121,403,430,122,174,405,50,406,409,123,41,42,271,124,410,419,169,224,175,309,274,420,421,275,43,176,422,128,428,129,131,59,45,178,179,225,132,283,180,52,60,194,61,263,260,63,203,64,181,65,66,190,296,204,310,289,206,242,258,261,262,284,285,286,290,291,297],
           [24,204,351,21,201,93,53,13,405,408,210,409,126,145,318,159,437,191,11,327,265,224,338,366,149,22,71,110,414,1,383,438,205,284,59,7,428,111,19,382,120,229,392,297,425,259,6,411,52,16,340,368,291,227,283,439,300,406,151,263,8,83,249,212,418,308,270,448,20,289,379,140,119,321,436,94,181,43,105,285,58,444,202,401,272,86,389,121,41,141,435,48,276,234,312,295,143,131,292,214,23,221,407,139,144,443,231,323,35,336,209,146,381,410,95,203,96,85,324,188,226,309,236,103,147,150,397,337,331,293,100,352,113,107,40,255,99,325,179,133,208,440,277,138,398,371,341,97,9,266,286,287,174,122,441,316,268,442,254,200,275,412,101,387,61,193,243,160,65,25,294,273,12,170,14,15,91,403,106,148,217,445,32,390,109,18,307,376,2,162,125,329,116,278,317,177,26,163,335,84,237,228,413,301,399,417,311,90,421,27,238,187,60,269,178,167,339,87,152,342,247,320,271,363,153,135,142,218,296,28,302,82,253,310,384,252,279,298,343,299,362,127,36,420,446,264,136,332,402,333,274,198,206,89,164,347,280,303,115,123,380,17,256,233,326,183,34,207,78,374,50,42,102,137,29,98,400,199,30,404,79,304,154,281,447,364,230,267,282,344,449,195,415,239,427,288,31,10,92,155,450,190,192,88,328,211,182,330,3,290,305,80,165,33,416,156,4,185,37,262,128,56,62,104,306,38,423,367,108,63,66,134,250,313,219,180,64,5,54,112,314,385,189,429,39,157,184,44,334,257,315,45,319,345,158,161,419,118,124,114,232,240,244,117,129,67,258,213,68,365,322,386,348,55,357,361,251,166,370,186,396,241,194,260,171,388,46,168,57,130,346,349,422,132,369,69,215,225,261,350,196,169,197,172,235,173,47,49,353,424,216,354,220,51,175,377,391,176,222,70,355,426,356,358,223,359,430,360,242,372,245,373,393,431,72,246,248,73,375,74,432,75,378,394,395,433,434,76,77,81],
           [76,232,307,1,130,402,343,85,300,61,352,65,365,344,23,356,112,184,393,407,291,397,60,237,209,161,329,398,248,176,245,375,408,101,376,86,104,320,222,6,381,175,70,347,68,145,304,231,380,247,187,221,246,249,59,3,9,387,399,256,164,250,181,172,400,158,309,51,79,80,108,10,254,230,409,373,426,261,153,355,109,391,177,353,188,236,410,251,224,357,52,388,202,284,162,149,43,20,252,122,151,359,182,7,138,139,379,113,2,134,69,110,74,253,66,312,83,73,111,358,30,212,295,233,45,58,382,88,77,179,262,279,87,442,285,276,183,266,440,185,401,62,345,75,360,11,386,40,84,95,403,114,306,294,346,351,354,271,41,29,53,301,308,140,348,142,15,78,12,5,310,13,115,205,82,21,267,71,116,350,165,57,64,19,361,406,421,302,278,63,330,331,413,189,72,311,383,135,384,441,141,240,448,305,46,131,377,313,200,35,213,415,144,327,36,44,283,67,404,163,119,277,92,89,81,211,389,47,349,368,90,91,210,93,390,255,268,364,168,16,405,431,31,94,314,96,186,143,174,132,362,293,14,48,427,125,257,414,223,203,332,315,286,146,392,275,395,258,190,117,272,191,97,363,280,411,22,98,147,193,259,99,37,260,148,100,436,447,25,207,199,412,102,103,105,55,416,106,316,204,263,192,394,417,137,273,366,155,396,107,367,194,235,433,54,374,49,38,369,120,243,169,118,370,264,226,17,216,321,378,24,128,160,418,133,296,287,121,4,225,171,371,18,8,333,123,385,425,124,372,126,419,127,227,420,422,449,423,195,424,297,214,129,56,228,229,428,136,317,429,430,150,299,432,152,178,26,154,206,159,27,303,156,157,166,28,167,170,434,435,173,322,180,196,437,438,439,281,197,328,234,198,443,201,32,208,265,215,217,33,238,239,444,445,446,34,450,218,219,39,42,298,318,220,50,274,241,242,244,288,269,334,270,282,289,290,292,319,323,324,325,326,335,336,337,338,339,340,341,342],
           [240,157,405,136,366,435,408,111,86,108,397,65,434,306,54,438,334,143,299,384,1,219,267,97,100,88,172,10,354,388,122,144,94,76,278,61,113,287,171,198,394,118,262,429,25,368,417,359,60,317,344,62,137,160,208,236,247,431,246,203,369,367,398,64,443,225,124,158,63,295,355,57,14,218,35,90,135,53,50,194,370,393,305,56,155,114,343,3,95,138,205,12,107,152,127,99,428,251,255,91,147,210,146,212,427,181,353,163,233,403,409,204,399,263,311,101,430,206,104,72,341,308,139,49,66,264,199,38,115,55,128,312,265,325,125,293,58,27,5,340,432,15,93,376,328,404,78,307,156,182,377,98,92,67,145,151,374,345,241,89,400,420,401,266,294,126,105,349,153,161,238,183,175,330,162,59,335,237,357,39,418,336,187,110,447,331,260,371,276,102,8,274,71,9,87,365,134,190,315,337,406,154,69,129,33,228,231,419,68,140,6,34,22,243,195,18,176,70,439,2,159,48,275,229,109,360,196,296,164,73,179,103,211,248,282,297,77,74,268,148,200,319,230,272,112,422,342,338,80,381,339,239,30,214,16,141,177,261,433,326,318,213,31,79,75,313,372,142,424,242,332,226,106,165,46,269,184,440,166,270,373,96,51,4,309,116,149,82,375,168,11,244,378,40,379,436,402,346,173,380,178,117,150,333,271,245,167,444,234,356,254,207,52,358,256,407,17,392,37,441,169,45,279,170,174,197,123,180,185,347,81,316,448,257,201,258,83,410,301,348,361,119,186,411,7,395,362,84,386,396,120,121,41,390,235,224,188,412,363,382,303,416,249,351,221,42,209,323,442,85,259,350,189,413,291,220,391,250,352,327,252,13,24,280,445,310,130,253,273,414,191,192,437,415,131,277,446,364,193,32,389,449,383,132,450,281,385,387,133,314,298,421,423,320,202,425,215,288,216,47,302,321,217,426,322,19,222,300,223,20,21,227,23,304,324,26,232,283,289,284,285,286,290,292,329,28,29,36,43,44],
           [332,158,74,150,37,380,90,219,278,308,124,207,66,63,109,425,431,327,305,320,208,47,56,390,157,163,409,179,448,266,398,381,423,73,80,62,54,169,333,384,78,57,192,195,120,353,221,152,229,127,75,435,173,181,426,330,395,385,110,392,200,111,374,225,182,3,286,288,223,167,222,352,275,412,96,394,366,368,148,144,44,273,183,268,55,209,147,449,142,309,391,396,418,313,168,201,367,58,38,191,274,310,92,97,324,239,93,240,156,241,383,251,114,165,68,170,372,267,166,116,125,159,59,94,71,226,292,39,280,382,230,102,242,321,198,115,160,342,354,369,184,337,171,296,51,287,65,24,103,231,139,279,438,197,370,60,25,263,98,355,194,376,61,36,297,256,151,6,199,104,424,386,440,140,227,95,28,293,117,185,123,306,9,112,52,377,220,128,243,316,32,434,294,91,20,141,397,224,202,145,325,172,76,365,362,356,7,389,196,174,121,371,27,129,30,131,106,250,258,347,175,289,387,10,430,4,203,378,276,399,126,149,118,204,64,29,105,119,417,349,291,138,269,317,318,350,447,422,153,307,373,375,205,302,428,176,357,177,154,186,130,277,388,244,23,45,319,178,162,338,132,2,26,400,379,340,348,419,363,99,281,283,14,21,187,441,248,143,228,401,323,402,232,311,234,301,351,107,79,67,439,206,113,69,210,33,403,100,53,393,211,328,252,259,404,40,303,249,180,70,212,108,13,31,410,298,405,312,406,72,364,407,315,81,77,82,122,83,215,164,421,11,101,233,270,133,260,188,341,41,245,146,155,314,218,161,189,213,12,190,257,427,193,214,84,216,290,217,247,85,429,271,134,135,42,408,235,358,136,236,442,411,343,137,304,237,339,86,413,359,262,272,414,415,443,34,238,282,246,444,416,284,264,87,420,360,43,253,322,254,361,295,255,299,35,50,88,432,261,18,326,46,300,265,433,285,329,331,334,335,336,344,436,89,345,346,48,437,49,445,446,450,1,5,8,15,16,17,19,22],
           [415,102,15,303,391,42,131,254,265,291,355,31,387,323,163,138,173,198,326,272,140,261,321,377,443,211,193,225,210,30,270,226,132,284,78,71,325,260,327,139,100,281,221,89,153,383,227,378,183,103,199,322,414,121,248,8,384,43,285,142,72,104,367,255,439,47,379,314,306,304,54,9,133,328,96,337,259,324,263,44,24,63,365,39,184,214,99,116,308,385,309,380,88,278,234,76,329,160,441,179,12,97,186,196,423,333,82,283,256,397,330,279,10,240,370,244,55,18,411,362,2,331,342,90,148,126,164,21,338,207,252,349,305,40,146,275,424,280,107,229,228,432,109,286,273,80,134,332,98,91,292,101,14,185,238,161,310,402,235,194,158,87,144,11,177,290,336,150,119,442,381,396,425,92,231,298,168,416,175,317,106,16,17,120,250,257,282,108,258,115,352,19,201,105,77,382,440,412,79,159,403,56,110,428,145,386,276,312,350,52,178,57,122,195,176,368,48,4,25,307,118,429,319,371,127,395,297,117,356,426,274,361,32,430,339,230,417,215,93,366,267,316,422,388,111,147,311,162,202,389,13,372,407,390,293,83,334,189,197,287,165,73,200,192,112,135,418,123,348,113,33,166,22,58,151,136,253,3,341,5,433,404,427,392,335,266,23,262,59,269,149,218,393,340,20,94,74,34,209,421,137,294,187,208,398,394,399,203,400,288,264,431,289,232,360,222,114,434,84,152,302,233,420,243,171,435,401,245,26,204,268,205,41,60,6,45,444,405,239,436,277,46,406,167,343,364,408,419,345,27,170,206,246,141,49,437,172,438,271,181,180,81,445,295,182,446,313,174,447,95,212,315,188,169,28,61,124,409,85,29,35,247,216,296,448,299,300,190,236,86,410,36,213,449,301,413,450,129,191,1,318,7,344,37,217,346,125,320,347,219,351,359,50,143,220,38,51,53,237,223,224,241,353,62,242,128,64,249,354,154,251,130,155,156,357,358,65,363,369,66,157,373,374,375,376,67,68,69,70,75],
           [30,286,202,312,276,446,20,261,187,307,13,8,18,188,158,186,92,204,73,300,143,151,431,441,319,248,56,62,55,216,91,85,51,344,448,378,339,19,189,75,324,252,134,341,438,292,128,79,97,253,432,239,4,411,281,323,260,337,436,315,154,129,1,256,21,449,183,359,15,423,36,338,224,169,280,212,63,10,290,159,262,270,397,317,283,279,190,93,217,226,9,370,354,11,175,426,6,358,335,22,382,371,410,155,140,291,366,203,352,258,360,163,130,357,29,412,191,269,105,402,96,112,322,52,120,46,27,177,5,413,196,386,332,207,94,23,100,58,274,2,367,184,215,47,141,243,59,326,113,214,330,263,379,201,311,48,298,389,275,355,351,72,293,232,282,433,305,430,95,131,434,12,362,195,106,53,39,218,435,205,31,309,14,407,111,376,57,16,316,329,365,219,401,206,49,284,238,405,264,331,135,240,388,50,35,98,150,74,310,132,333,340,40,342,347,152,320,403,160,185,285,76,450,230,334,54,60,117,61,372,64,192,161,437,287,246,78,439,373,440,164,249,380,208,193,277,404,65,278,114,244,107,241,294,387,170,393,66,343,447,417,384,182,178,420,17,424,99,67,345,139,213,142,68,415,336,391,421,443,220,84,288,374,375,133,308,146,77,356,33,119,377,24,353,101,41,422,80,194,25,26,328,289,156,445,301,89,385,271,136,209,406,425,125,346,102,34,28,223,442,108,394,363,126,296,69,221,265,197,408,348,210,295,168,414,349,32,103,318,297,234,70,242,211,245,172,361,299,247,179,268,409,122,180,137,37,250,350,364,38,306,222,235,198,444,199,81,71,368,3,369,138,82,200,390,381,416,302,225,259,83,7,227,228,233,383,266,86,251,147,109,157,418,396,392,419,229,42,43,90,87,427,231,171,236,237,88,162,104,257,428,173,313,254,429,144,145,255,267,44,395,398,148,399,325,110,400,115,149,45,165,272,116,118,121,123,273,124,303,127,314,304,153,166,167,174,176,321,327,181]]
user_file_TRset = ['C:/Users/USER/bear/Experiment03E - increasing sizes - 10 users/EXPERIMENT03 - User01 - TRset450.csv', 'C:/Users/USER/bear/Experiment03E - increasing sizes - 10 users/EXPERIMENT03 - User02 - TRset450.csv', 'C:/Users/USER/bear/Experiment03E - increasing sizes - 10 users/EXPERIMENT03 - User03 - TRset450.csv', 'C:/Users/USER/bear/Experiment03E - increasing sizes - 10 users/EXPERIMENT03 - User04 - TRset450.csv', 'C:/Users/USER/bear/Experiment03E - increasing sizes - 10 users/EXPERIMENT03 - User05 - TRset450.csv', 'C:/Users/USER/bear/Experiment03E - increasing sizes - 10 users/EXPERIMENT03 - User06 - TRset450.csv', 'C:/Users/USER/bear/Experiment03E - increasing sizes - 10 users/EXPERIMENT03 - User07 - TRset450.csv', 'C:/Users/USER/bear/Experiment03E - increasing sizes - 10 users/EXPERIMENT03 - User08 - TRset450.csv', 'C:/Users/USER/bear/Experiment03E - increasing sizes - 10 users/EXPERIMENT03 - User09 - TRset450.csv', 'C:/Users/USER/bear/Experiment03E - increasing sizes - 10 users/EXPERIMENT03 - User10 - TRset450.csv']
user_file_TESTset = ['C:/Users/USER/bear/Experiment03E - increasing sizes - 10 users/EXPERIMENT03 - User01 - TESTset LAST50 no Header.csv','C:/Users/USER/bear/Experiment03E - increasing sizes - 10 users/EXPERIMENT03 - User02 - TESTset LAST50 no Header.csv','C:/Users/USER/bear/Experiment03E - increasing sizes - 10 users/EXPERIMENT03 - User03 - TESTset LAST50 no Header.csv','C:/Users/USER/bear/Experiment03E - increasing sizes - 10 users/EXPERIMENT03 - User04 - TESTset LAST50 no Header.csv','C:/Users/USER/bear/Experiment03E - increasing sizes - 10 users/EXPERIMENT03 - User05 - TESTset LAST50 no Header.csv','C:/Users/USER/bear/Experiment03E - increasing sizes - 10 users/EXPERIMENT03 - User06 - TESTset LAST50 no Header.csv','C:/Users/USER/bear/Experiment03E - increasing sizes - 10 users/EXPERIMENT03 - User07 - TESTset LAST50 no Header.csv','C:/Users/USER/bear/Experiment03E - increasing sizes - 10 users/EXPERIMENT03 - User08 - TESTset LAST50 no Header.csv','C:/Users/USER/bear/Experiment03E - increasing sizes - 10 users/EXPERIMENT03 - User09 - TESTset LAST50 no Header.csv','C:/Users/USER/bear/Experiment03E - increasing sizes - 10 users/EXPERIMENT03 - User10 - TESTset LAST50 no Header.csv']
number_of_features_per_user = [49, 50, 50, 48, 51, 48, 50, 50, 49, 45]
#Results file
workbook = xlsxwriter.Workbook('C:/Users/USER/bear/RandomForest Regressor Results-10users-20-11-20.xlsx')
worksheets = [workbook.add_worksheet() for i in range(1)]
worksheets[0].write(0, 0, "Size of the learning set")
worksheets[0].write(0, 1, "Average error 10 users")

#starting from L=6
partial_training_set_size = 0
while partial_training_set_size < partial_training_set_size_max:
    user_num = 0
    average_prediction_error_per_user = 0
    partial_training_set_size += 1
    while user_num < number_of_users: 
        worksheets[0].write(0, 11 * user_num + 2, "user Random Forest Average error")
        worksheets[0].write(0, 11 * user_num + 3, "Random Forest Average error for test 1")
        worksheets[0].write(0, 11 * user_num + 4, "Random Forest Average error for test 2")
        worksheets[0].write(0, 11 * user_num + 5, "Random Forest Average error for test 3")
        worksheets[0].write(0, 11 * user_num + 6, "Random Forest Average error for test 4")
        worksheets[0].write(0, 11 * user_num + 7, "Random Forest Average error for test 5")
        worksheets[0].write(0, 11 * user_num + 8, "Random Forest Average error for test 6")
        worksheets[0].write(0, 11 * user_num + 9, "Random Forest Average error for test 7")
        worksheets[0].write(0, 11 * user_num + 10, "Random Forest Average error for test 8")
        worksheets[0].write(0, 11 * user_num + 11, "Random Forest Average error for test 9")
        worksheets[0].write(0, 11 * user_num + 12, "Random Forest Average error for test 10")
        print('user_num=',user_num)
        print('partial_training_set_size=',partial_training_set_size)
        set_num = 0
        average_prediction_error_per_set = 0
        output_column_position = 1
        while set_num < number_of_tests_per_size:
#            print('set_num=',set_num)
#Creating the input file
            with open(user_file_TRset[user_num], encoding='utf8', newline='') as csvfile:
                table_d = csv.reader(csvfile)
                table_data = list(table_d)

            with open(user_file_TESTset[user_num], encoding='utf8', newline='') as csvfile_test:
                table_t = csv.reader(csvfile_test)
                table_test = list(table_t)

            with open('C:/Users/USER/bear/Experiment03E - increasing sizes - 10 users/EXPERIMENT03E Scikit-fixed Test set and var Training set.csv', 'w', newline='') as f_test:
                writer = csv.writer(f_test)
                writer.writerow(table_data[0])

            l_num = 0
            while l_num < test_set_size:
                with open('C:/Users/USER/bear/Experiment03E - increasing sizes - 10 users/EXPERIMENT03E Scikit-fixed Test set and var Training set.csv', 'a', newline='') as f_test:
                    writer = csv.writer(f_test)
                    writer.writerow(table_test[l_num])
                l_num += 1
            f_test.close

                     
# Lines of the input file
            items_num = 0
            line_position = 1
            while items_num < partial_training_set_size:
                items_num += 1                
                with open('C:/Users/USER/bear/Experiment03E - increasing sizes - 10 users/EXPERIMENT03E Scikit-fixed Test set and var Training set.csv', 'a', newline='') as f:
 #                   print('items_num=', items_num)
                    writer = csv.writer(f)
                    writer.writerow(table_data[r_lines[set_num][items_num - 1]])

                line_position +=1                             
            f.close()

            dataset = pd.read_csv('C:/Users/USER/bear/Experiment03E - increasing sizes - 10 users/EXPERIMENT03E Scikit-fixed Test set and var Training set.csv')
            x = dataset.iloc[:, 0:number_of_features_per_user[user_num]].values
            y = dataset.iloc[:, number_of_features_per_user[user_num]].values

            sheet_num = 0
# Train on the samples 50 to the end, test on the first 50 samples.
#[50] specifies the index at which the array is splitted.
            x_test, x_train = np.array_split(x, [50])
            y_test, y_train = np.array_split(y, [50])

            scl = StandardScaler()
            x_train = scl.fit_transform(x_train)
            x_test = scl.transform(x_test)                              
            clf = RandomForestRegressor(n_estimators = 100, random_state = 0)
            clf = clf.fit(x_train, y_train)      
            y_pred = clf.predict(x_test)
            average_prediction_error = 0
            sum_of_prediction_errors = 0
        
        
            for i in range(0, test_set_size): 
                sum_of_prediction_errors += abs(y_test[i] - round(y_pred[i],0))
       
            average_prediction_error = sum_of_prediction_errors / test_set_size
            average_prediction_error_per_set = average_prediction_error_per_set + average_prediction_error
            output_column_position +=1
            worksheets[sheet_num].write(partial_training_set_size, (11 * user_num) + output_column_position, average_prediction_error)

            set_num += 1

        worksheets[sheet_num].write(partial_training_set_size, 0, partial_training_set_size)
        average_prediction_error_per_set = average_prediction_error_per_set / number_of_tests_per_size
        worksheets[sheet_num].write(partial_training_set_size,(11 * user_num) + output_column_position - number_of_tests_per_size, average_prediction_error_per_set)
        average_prediction_error_per_user += average_prediction_error_per_set
        user_num += 1
    worksheets[sheet_num].write(partial_training_set_size, 1, average_prediction_error_per_user / number_of_users)
workbook.close()


