#!/usr/local/bin/python3.4
"""
Name: 
Purpose: checks Answers
Author: Jurre Hageman
Created: 24/03/2015
"""
#imports


def checkAnwers(student_answers, model):
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