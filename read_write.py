import time
import csv
import sys
from bs4 import BeautifulSoup
import warnings
warnings.filterwarnings('ignore', category=
                        UserWarning, module='bs4')

def delete_html_tags(file_name):
    f = open(file_name, 'rt', encoding="utf16") # opens the csv file
    reader = csv.reader(f, delimiter='\t', quoting=csv.QUOTE_NONE)  # creates the reader object

    data = []

    for line in reader:
        new_line = []
        if line[0] != "Gebruikersnaam":
            for element in line:
                soup = BeautifulSoup(element, 'html.parser')
                strip = soup.get_text()
                new_line.append(strip)
            data.append(new_line)
    return data


def antwoorden(antwoordFile):
    antwoorden = {}
    for num, line in enumerate(open(antwoordFile, "r")):
        line = line.rstrip("\n").split(";")
        item = [i.strip() for i in line]
        antwoorden.update({num+1:item})
    return antwoorden


def create_student_list(data):
    students = []
    for line in data:

        naw_number = line[0]
        sur_name = line[1]
        first_name = line[2]
        group_inf = line[-10].split("-")
        group_inf = [i.strip().strip('"') for i in group_inf]
        group = group_inf[0]
        subgroup = group_inf[1]
        answers = line[5::6]
        # modify number 1
        for num, answer in enumerate(answers):
            if answer.strip() == "1":
                answers[num] = "number: 1"
        students.append({
            'naw_number': naw_number,
            'sur_name' : sur_name,
            'first_name' : first_name,
            'group' : group,
            'subgroup' : subgroup,
            'answers' : answers})
    return students



def write_csv(students, outFile):
    try:
        ofile  = open(outFile, "w")
        header = ("Studentnummer", "Achternaam", "Voornaam", "Groep", "Subgroep","Aantal vragen", "Score")
        vraag = ["vraag " + str(i+1) for i in range(len(students[0]['answers']))]
        writer = csv.writer(ofile, delimiter=';', quotechar='"', quoting=csv.QUOTE_ALL)
        writer.writerow((header + tuple(vraag)))
        for student in students:
            data = []
            data.append(student['naw_number'])
            data.append(student['sur_name'])
            data.append(student['first_name'])
            data.append(student['group'])
            data.append(student['subgroup'])
            data.append(len(student['answers']))
            data.append(student['student_score']['score'])
            for num, antwoord in sorted(student['student_score']['score_per_question'].items()):
                data.append(antwoord)
            writer.writerow(data)
        #statistics
        writer.writerow(())
        writer.writerow(())
        writer.writerow(("Resultaten nakijkscript", ""))
        writer.writerow(("outFile", outFile))
        writer.writerow(("Date",time.strftime("%d/%m/%Y")))
        writer.writerow(("Time",time.strftime("%H:%M:%S")))
        writer.writerow(("Aantal studenten",len(students)))
    finally:
        ofile.close()
