# coding: utf-8

from __future__ import division
from itertools import combinations
import re

class Solver:

    target = 24
    ops = ['+', '-', '*', '/', '--', '//']

    def __init__(self, precise_mode=False):
        self.precise_mode = precise_mode

    def solution(self, nums):
        result = []
        groups = self.dimensionality_reduction(self.format(nums))
        for group in groups:
            for op in self.ops:
                exp = self.assemble(group[0], group[1], op)['exp']
                if self.check(exp, self.target) and exp not in result:
                    result.append(exp)
        return [exp + '=' + str(self.target) for exp in result]

    def dimensionality_reduction(self, nums):
        result = []
        if len(nums) > 2:
            for group in self.group(nums, 2):
                for op in self.ops:
                    new_group = [self.assemble(group[0][0], group[0][1], op)] + group[1]
                    result += self.dimensionality_reduction(new_group)
        else:
            result = [nums]
        return result

    def assemble(self, exp1, exp2, op):
        if op == '--' or op == '//':
            return self.assemble(exp2, exp1, op[0])

        if op in r'*/':
            exp1 = self.add_parenthesis(exp1)
            exp2 = self.add_parenthesis(exp2)

        if self.precise_mode:
            if op == '-':
                exp2 = self.add_parenthesis(exp2)
            elif op == '/':
                exp2 = self.add_parenthesis(exp2, True)

        exp = self.convert(exp1['exp'] + op + exp2['exp'], op)
        return {'op': op, 'exp': exp}

    @staticmethod
    def add_parenthesis(exp, is_necessary=False):
        if (is_necessary and not exp['exp'].isdigit()) or exp['op'] in r'+-':
            result = {
                'exp': '(' + exp['exp'] + ')',
                'op': exp['op']
            }
        else:
            result = exp
        return result

    @staticmethod
    def check(exp, target, precision=0.0001):
        try:
            return abs(eval(exp) - target) < precision
        except ZeroDivisionError:
            return False

    @staticmethod
    def convert(exp, op):
        if op in r'+-':
            pattern = r'([\+\-]((\(.+\)|\d+)[\*\/](\(.+\)|\d+)|\d+))'
            exp = '+' + exp
        else:
            pattern = r'([\*\/](\(.+?\)|\d+))'
            exp = '*' + exp
        result = ''.join(sorted([i[0] for i in re.findall(pattern, exp)]))
        if len(result) != len(exp):
            result = exp
        return result[1:]

    @staticmethod
    def format(nums):
        return [{'op': ' ', 'exp': str(num)} for num in nums]

    @staticmethod
    def group(exp_list, counter):
        index_list = [i for i in range(len(exp_list))]
        combination = list(combinations(index_list, counter))
        for group1 in combination:
            group2 = list(set(index_list) - set(group1))
            yield [
                [exp_list[g1] for g1 in group1],
                [exp_list[g2] for g2 in group2]
            ]
### test
# customer_input = [4,3,10,10]
# task = Solver()
# answer = task.solution(customer_input)
#
# if len(answer) == 0:
#     print('No solutions')
# else:
#     for a in answer:
#         print(a)
