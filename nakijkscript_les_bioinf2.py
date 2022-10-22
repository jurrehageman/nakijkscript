#!/usr/bin/env python3
"""
Name: nakijkscript.py
Purpose: nakijken bioinfo opgaven.
Author: Jurre Hageman and Mark Sibbald
Created: 2015-03-21
Updated: 2022-10-20
"""

#imports
import xlsxwriter
import os.path
import argparse
import time
import csv
import sys
import warnings
warnings.filterwarnings('ignore', category=
                        UserWarning, module='bs4')
import pandas as pd
t0 = time.time()


def args():
    "parses command line arguments"
    parser = argparse.ArgumentParser(description="checks student answers")
    parser.add_argument("in_file", help="the path to the File with the input")
    parser.add_argument("out_file", help="the path to the File with the output")
    parser.add_argument("antwoord_file", help="the answer file")
    args = parser.parse_args()
    return args


def check_anwers(student_answers, model):
    score = 0
    score_dict = {}
    for num, answer in enumerate(student_answers):
        answer = answer.strip()
        if answer in model[num+1]:
            score += 1
            score_dict.update({num+1:1})
        else:
            score_dict.update({num+1:student_answers[num]})
    res = { 'score' : score, 'score_per_question' : score_dict}
    return res


def read_answers(antwoordfile):
    antwoorden = {}
    for num, line in enumerate(open(antwoordfile, "r")):
        line = line.rstrip("\n").split(";")
        item = [i.strip() for i in line]
        antwoorden.update({num+1:item})
    return antwoorden


def create_student_list(data):
    students = []
    for index, row in data.iterrows():
        row = list(row)
        time_start = row[1]
        time_stop = row[2]
        naw_number = row[-3]
        name = row[4]
        group = row[-2]
        subgroup = row[-1]
        answers = row[5:]
        answers = answers[:-3]
        answers = [str(i) for i in answers]
        for num, answer in enumerate(answers):
                if answer.strip() == "1":
                    answers[num] = "number: 1"   
        students.append({
            'naw_number': naw_number,
            'name' : name,
            'group' : group,
            'subgroup' : subgroup,
            'answers' : answers})
    return students


def read_xlsx(file_name):
    excel_data = pd.read_excel(file_name, sheet_name="Form1")
    data = pd.DataFrame(excel_data)
    return data

def write_xlsx(students, outFile):
    try:
        ofile = open(outFile, "w")
        workbook = xlsxwriter.Workbook(outFile)
        worksheet = workbook.add_worksheet('Nakijken Bioinformatica 2')

        info = ["Studentnummer", "Naam", "Klas", "Groep", "Aantal vragen", "Score"]
        vraag = ["vraag " + str(i+1) for i in range(len(students[0]['answers']))]
        headers = info + vraag
        results_list = []
        for student in students:
            data = []
            data.append(student['naw_number'])
            data.append(student['name'])
            data.append(student['group'])
            data.append(student['subgroup'])
            data.append(len(student['answers']))
            data.append(student['student_score']['score'])
            for num, antwoord in sorted(student['student_score']['score_per_question'].items()):
                data.append(antwoord)
            results_list.append(data)

        results_list.insert(0, headers)
        for row_num, row_data in enumerate(results_list):
            for col_num, col_data in enumerate(row_data):
                worksheet.write(row_num, col_num, col_data)
        workbook.close()
    finally:
        ofile.close()



def main():
    comm_args = args()
    in_file = comm_args.in_file
    out_file = comm_args.out_file
    antwoord_file = comm_args.antwoord_file
    #text_stripped = delete_html_tags(in_file)
    df = read_xlsx(in_file)
    students = create_student_list(df)
    answer_model = read_answers(antwoord_file)

    for student in students:
        print("processing: {}, {}".format(student['naw_number'], student['name']))
        if len(answer_model) != len(student['answers']):
            print("WAARSCHUWING: aantal antwoorden antwoordmodel: ({}) is niet gelijk aan het aantal antwoorden ({}) van student: {}".format(len(answer_model),len(student['answers']), student['name']))
            sys.exit(1)
        student_score = check_anwers(student['answers'], answer_model)
        student['student_score'] = student_score
    if os.path.isfile("{}".format(out_file)):
        print("File {} bestaat al".format(out_file))
        #response = 'y'
        response = input("Overschrijven? y/n: ")
        if response == "y":
            write_xlsx(students, out_file)
        else:
            sys.exit(0)
    else:
        write_xlsx(students, out_file)
    print('\nRuntime lasted {0:.1f} sec'.format(time.time()-t0))


if __name__ == "__main__":
    main()
