#!/usr/bin/env python
# -*- coding:gbk -*-
import pandas as pd  
 
clean_data = []  
def select_dataposition():  
    data = pd.read_csv('51job-data_analysis.csv',header = 0,encoding= 'gbk')  
    df = pd.DataFrame(data)  
    # df = df[df.position.str.contains(r'.*?数据.*?|.*?分析。*？')]  
    #df = df[df.dropna(df.salary ='')]  
    df.to_excel('data_51.xlsx')  
def get_file_elements():  
    file = pd.read_excel('data_51.xlsx')  
    file = pd.DataFrame(file)  
    rows = len(file)  
    print rows 
    for i in range(0, rows):  
        raw_data = {}  
        raw_data['company'] = file['company'][i]  
        raw_data['name'] = file['name'][i]  
        if '-' in file['work_place'][i]:  
            plc_1 = str(file['work_place'][i]).find('-')  
            raw_data['city'] = file['work_place'][i][:plc_1]  
        else:  
            raw_data['city'] = file['work_place'][i]  
#        print(file['salary'][i])  
        if file['salary'][i] == "":  
            raw_data['low_salary'] = ''  
            raw_data['high_salary'] = ''  
        elif '-' in file['salary'][i]:  
            plc_2 = str(file['salary'][i]).find('-')  
            low_salary = file['salary'][i][:plc_2]  
            high_salary = file['salary'][i][plc_2 + 1 :].rstrip('万/月|千/月|万/年|天')  
    #       print(raw_data['high_salary'])  
            if '万/月' in file['salary'][i]:  
                raw_data['low_salary'] = float(low_salary) * 10  
                raw_data['high_salary'] = float(high_salary) * 10  
            elif '千/月' in file['salary'][i]:  
                raw_data['low_salary'] = float(low_salary)  
                raw_data['high_salary'] = float(high_salary)  
            elif '万/年' in file['salary'][i]:  
                raw_data['low_salary'] = float(low_salary) * 10 / 12  
                raw_data['high_salary'] = float(high_salary) * 10 / 12
            elif '天' in file['salary'][i]:
                raw_data['low_salary'] = float(low_salary) * 30
                raw_data['high_salary'] = float(high_salary) * 30  
        elif '天' in file['salary'][i]:
            raw_data['low_salary'] = float(low_salary) * 30
            raw_data['high_salary'] = float(high_salary) * 30
        else:
            raw_data['low_salary'] = file['salary'][i]
            raw_data['high_salary'] = file['salary'][i]
        raw_data['company_link'] = file['company_link'][i]  
        raw_data['publish_time'] = file['publish_time'][i]  
        clean_data.append(raw_data)  
        print('Processing with line ' + str(i) + '------')  
        print('Still have ' + str(rows + 1 - i) + ' rows to complete------')  
    return clean_data  
def save_clean_data(clean_data):  
    lt = pd.DataFrame(clean_data)  
    lt.to_excel('final_result.xlsx')  
    print("Successfully Saved My File!")  
#select_dataposition() 
#clean_data = get_file_elements()  
#save_clean_data(clean_data)  
def top():
    file = pd.read_excel('final_result.xlsx')
    file = pd.DataFrame(file)  
    rows = len(file)
    top_data = []
    raw_data = {}
    for i in range(0, rows):  
        if file['city'][i] in top_data:
            raw_data(file['city'][i]) += 1
        else:
            raw_data(file['city'][i]) = 1
    print raw_data