#!/usr/bin/env python3
"""
Name: nakijkscript.py
Purpose: nakijken bioinfo opgaven.
Author: Jurre Hageman and Mark Sibbald
Created: 2015-03-21
Updated: 2022-10-22
"""

#imports
import xlsxwriter
import argparse
import time
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


def check_anwers(students):
    for student in students:
        scores = []
        for num, answer in enumerate(student['answers']):
            if answer in student['answermodel'][num +1]:
                scores.append(1)
            else:
                scores.append(0)    
        student['scores'] = scores


def read_answers(antwoordfile):
    antwoorden = {}
    for num, line in enumerate(open(antwoordfile, "r")):
        line = line.rstrip("\n").split(";")
        item = [i.strip() for i in line]
        antwoorden.update({num+1:item})
    return antwoorden


def create_student_list(data, answer_model):
    students = []
    columns = list(data.columns)
    questions = []
    for i in columns:
        if i.startswith("Question"):
            questions.append(i.split("\xa0")[-1].strip())
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
        students.append({
            'time_start': str(time_start),
            'time_stop': str(time_stop),
            'naw_number': naw_number,
            'name': name,
            'group': group,
            'subgroup': subgroup,
            'questions': questions,
            'answermodel': answer_model,
            'answers': answers,
            'scores': None})
    return students


def read_xlsx(file_name):
    excel_data = pd.read_excel(file_name, sheet_name="Form1")
    data = pd.DataFrame(excel_data)
    return data


def write_xlsx(students, outFile):
    #calc cell numbers for formula to calculate points
    num_of_questions = len(students[0]['questions'])
    start = 12 # column M
    end = num_of_questions * 4 + 12 # + 12 because first column with points is at 12 (0-based index) 
    step = 4 # every fourth column has points
    cell_nums = [i for i in range(start, end, step)]
    cell_letters = [xlsxwriter.utility.xl_col_to_name(i) for i in cell_nums]
    try:
        ofile = open(outFile, "w")
        workbook = xlsxwriter.Workbook(outFile)
        worksheet = workbook.add_worksheet('Nakijken Bioinformatica 2')
        info = ["Studentnummer", "Naam", "Klas", "Groep", "Start tijd", "Eind tijd", "Aantal vragen", "Score", "% Score"]
        vraag = []
        for i in range(len(students[0]['questions'])):
            vraag.append('vraag ' + str(i+1))
            vraag.append('model antwoord vraag ' + str(i+1))
            vraag.append('antwoord vraag ' + str(i+1))
            vraag.append('punten vraag ' + str(i+1))
        headers = info + vraag
        results_list = []
        for num, student in enumerate(students):
            data = []
            data.append(student['naw_number'])
            data.append(student['name'])
            data.append(student['group'])
            data.append(student['subgroup'])
            data.append(student['time_start'])
            data.append(student['time_stop'])
            data.append(len(student['answers']))
            #data.append(sum(student['scores']))
            cells = ",".join([i + str(num+2) for i in cell_letters])
            data.append(f"=sum({cells})") 
            data.append("=H" + str(num + 2) + "/" + str(num_of_questions) + "*100") 
            for i in range(len(students[0]['questions'])):                
                data.append(student['questions'][i])
                data.append(", ".join(student['answermodel'][i+1]))
                data.append(student['answers'][i])
                data.append(student['scores'][i])
            results_list.append(data)
        results_list.insert(0, headers)
        for row_num, row_data in enumerate(results_list):
            for col_num, col_data in enumerate(row_data):
                worksheet.write(row_num, col_num, col_data)
        # keep the following code in because I am not sure if the above code in the for loop will work to create Excel files.
        # the code above is without the worksheet.write function
        # the following is with the worksheet.write function but then a new for loop is used
        # for i in range(len(students)):
        #     dest = 'H' + str(i+2)            
        #     cells = [j + str(i+2) for j in cell_letters]
        #     formula = f'=sum({",".join(cells)})'
        #     worksheet.write_formula(dest, formula)
        colnames = []
        for i in headers:
            colnames.append({'header': i})
        worksheet.add_table(0, 0, row_num - 1, col_num, {'columns': colnames})
        workbook.close()
    finally:
        ofile.close()


def main():
    comm_args = args()
    in_file = comm_args.in_file
    out_file = comm_args.out_file
    antwoord_file = comm_args.antwoord_file
    answer_model = read_answers(antwoord_file)
    df = read_xlsx(in_file)
    students = create_student_list(df, answer_model)
    check_anwers(students)
    for student in students:
        print("processing: {}, {}".format(student['naw_number'], student['name']))
    write_xlsx(students, out_file)
    print('\nRuntime lasted {0:.1f} sec'.format(time.time()-t0))
    print("Done...")

if __name__ == "__main__":
    main()
