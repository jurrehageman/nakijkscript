#!/usr/bin/env python3
"""
Name: nakijkscript.py
Purpose: nakijken bioinfo opgaven.
Author: Jurre Hageman and Mark Sibbald
Created: 2015-03-21
Updated: 2020-01-27
"""

#imports
import time
import sys
import check_answers
import read_write
import os.path
import argparse
t0 = time.time()


def args():
    "parses command line arguments"
    parser = argparse.ArgumentParser(description="checks student answers")
    parser.add_argument("in_file", help="the path to the File with the input")
    parser.add_argument("out_file", help="the path to the File with the output")
    parser.add_argument("antwoord_file", help="the answer file")
    args = parser.parse_args()
    return args

def main():
    comm_args = args()
    in_file = comm_args.in_file
    out_file = comm_args.out_file
    antwoord_file = comm_args.antwoord_file
    text_stripped = read_write.delete_html_tags(in_file)
    students = read_write.create_student_list(text_stripped)
    answer_model = read_write.antwoorden(antwoord_file)

    for student in students:
        print("processing: {}, {}, {}".format(student['naw_number'], student['sur_name'], student['first_name']))
        if len(answer_model) != len(student['answers']):
            
            print("WAARSCHUWING: aantal antwoorden antwoordmodel: ({}) is niet gelijk aan het aantal antwoorden ({}) van student: {} {}".format(len(answer_model),len(student['answers']), student['sur_name'], student['first_name']))
            sys.exit(1)
        student_score = check_answers.checkAnwers(student['answers'], answer_model)
        student['student_score'] = student_score
    if os.path.isfile("{}".format(out_file)):
        print("File {} bestaat al".format(out_file))
        response = 'y'
        #response = input("Overschrijven? y/n: ")
        if response == "y":
            read_write.write_csv(students, out_file)
        else:
            sys.exit(0)
    else:
        read_write.write_csv(students, out_file)
    print('\nRuntime lasted {0:.1f} sec'.format(time.time()-t0))
        
if __name__ == "__main__":
    main()