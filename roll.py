#!/usr/bin/python3
# -*- coding: utf-8 -*-

import re
from random import randint
import operator

def fix_dice_string(source):
    '''
    :param Перебираем строку, приводим ее в годный вид
    :return функцию с годным списком
    '''
    def fix_now(string):
        string.replace(' ', '')
        dice_string = ''
        for i in string:
            if i == '+':
                i = ',+,'
            if i == '-':
                i = ',-,'
            if i == 'd':
                try:
                    int(dice_string[len(dice_string)-1])
                except:
                    dice_string += '1'
            dice_string += i
        ready_to_roll = re.split(',*', dice_string)
        return source(ready_to_roll)
    return fix_now

def roll(func):
    '''
    :param получаем функцию с исправленной строкой из fix_dice_string
    :return возвращаем функцию со списком, с наброшенными значениями
    '''
    def roll_now(roll_list):
        result_list = []
        for i in roll_list:
            result = 0
            check_d = re.search(r'd+', i, flags=re.IGNORECASE)
            try:
                if check_d.group(0) == 'd':
                    temp_list = re.split(r'd', i, flags=re.IGNORECASE)
                    for dice in range(int(temp_list[0])):
                        result += randint(1,int(temp_list[1]))
                    result_list.append(result)
            except:
                try:
                    result_list.append(int(i))
                except:
                    result_list.append(i)
        return func(result_list)
    return roll_now

def fix_list(func):
    '''
    :param забираем функцию с выроленными значениями из roll
    :return: возвращаем списк с операндами
    '''
    def fix_now(dice_string):
        new_string = []
        check_exp = None
        dice_string.insert(0, '+')
        for i in dice_string:
            if type(i) == int:
                new_string.append(i)
                continue
            if check_exp == i:
                continue
            else:
                new_string.append(i)
            check_exp = i
        return func(new_string)
    return fix_now

@fix_dice_string
@roll
@fix_list
def roll_result(result_list):
    '''
    :param получаем полностью готовый список для польской записи
    :return: готовую сумму, выполненную по правилам польской записи
    '''
    operators = {'+': operator.add, '-': operator.sub}
    result = 0
    current_operator = None
    for i in result_list:
        if type(i) == int:
            if current_operator == operator.add:
                result = current_operator(result, i)
            else:
                result = current_operator(result, i)
        else:
            current_operator = operators.get(i)
    return result

dice_string = "1d20 +d6-1d2+d100-10" ## тестовая строка
print(roll_result(dice_string)) ## тестовая строка
