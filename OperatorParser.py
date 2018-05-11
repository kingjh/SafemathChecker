# -*- coding: utf-8 -*-
import os
import re


def add(x, y):
    return x + ".add(" + y + ")"


def sub(x, y):
    return x + ".sub(" + y + ")"


def mul(x, y):
    return x + ".mul(" + y + ")"


def div(x, y):
    return x + ".div(" + y + ")"


def add_spaces_operator(matched):
    return " " + matched.group("operator") + " "


def add_spaces_left_bracket(matched):
    # add space after left bracket
    return matched.group("operator") + " "


def add_spaces_right_bracket(matched):
    # add space before right bracket
    return " " + matched.group("operator")


class OperatorParser:
    ops_rule = {
        "+": 1,
        "-": 1,
        "*": 2,
        "/": 2
    }

    operators = {"+": add, "-": sub, "*": mul, "/": div}

    def replace_operators(self, instr):
        """ replace basic math operators by SafeMath operators """
        # change ++, -- to add(1), sub(1)
        instr = re.sub(r"\+\+", ".add(1)", instr)
        instr = re.sub(r"--", ".sub(1)", instr)

        m1 = re.search(r"[+\-*/]=", instr)
        result = ""
        if m1:
            # handle the string with +=, -=, *=. /=
            v = instr[: m1.start()].rstrip(" ")
            v1 = v.strip(" ")
            expressions = [v1, m1.group()[: 1], "(", instr[m1.end():].strip().strip(";"), ");"]
            instr = v + "= " + " ".join(expressions)

        # split by !, &&, ||
        equations = re.split(r"(!|&&|\|\||)", instr)
        for equation in equations:
            # split by <=, >=, ==, !=, =
            expressions = re.split(r"([<>=!]*=)", equation)
            if len(expressions) == 1:
                result += equation
            else:
                for expression in expressions:
                    if re.search(r"[+\-*/]", expression):
                        # with math operators
                        # 0.exclude ;
                        rc = ""
                        pos = expression.find(';')
                        if pos != -1:
                            rc = expression[pos:]
                            expression = expression[:pos]

                        # 1.exclude independent ( or )
                        lbc = expression.count("(")
                        rbc = expression.count(")")
                        lc = ""
                        if lbc > rbc:
                            # ( is more than )
                            pos = expression.replace('(', 'X', lbc - rbc - 1).find('(')
                            lc = expression[: pos + 1]
                            expression = expression[pos + 1:]
                        else:
                            if lbc < rbc:
                                # ( is less than )
                                pos = 'X'.join(expression.rsplit(')', rbc - lbc - 1)).rfind(')')
                                rc = expression[pos:] + rc
                                expression = expression[:pos]

                        # 2.change normal notation to RPN, in order to change math operators to SafeMath operators
                        # 3.change RPN to normal notation
                        result += lc + self.rpn_to_nn(self.nn_to_rpn(expression)) + rc
                    else:
                        result += expression

        return result

    def nn_to_rpn(self, nn):
        """ change normal notation to a reverse polish notation """
        expression = []
        ops = []

        # handle +-*/) to add a space before and after the operator
        nn = nn.strip()
        nn = re.sub(r"(?P<operator>[+\-*/])", add_spaces_operator, nn)
        # handle the wrongly replaced " *  * "(maybe many spaces around *) to "**"
        nn = re.sub(r" *\* {2}\* *", "**", nn)
        nn = re.sub(r"(?P<operator>[(])", add_spaces_left_bracket, nn)
        nn = re.sub(r"(?P<operator>[)])", add_spaces_right_bracket, nn)
        items = re.split(r"\s+", nn)
        for item in items:
            if item in ["+", "-", "*", "/"]:
                while len(ops) >= 0:
                    if len(ops) == 0:
                        ops.append(item)
                        break
                    op = ops.pop()
                    if op == "(" or self.ops_rule[item] > self.ops_rule[op]:
                        ops.append(op)
                        ops.append(item)
                        break
                    else:
                        expression.append(op)
            elif item == "(":
                ops.append(item)
            elif item == ")":
                while len(ops) > 0:
                    op = ops.pop()
                    if op == "(":
                        break
                    else:
                        expression.append(op)
            else:
                expression.append(item)

        while len(ops) > 0:
            expression.append(ops.pop())

        return expression

    def f(self, x, o, y):
        return self.operators.get(o)(x, y)

    def rpn_to_nn(self, expressions):
        """ change reverse polish notation to normal notation, replace the math operators by SafeMath operators """
        stack = []
        for val in expressions:
            if val in self.operators.keys():
                y = stack.pop()
                x = stack.pop()
                stack.append(self.f(x, val, y))
            else:
                stack.append(val)

        return stack.pop()
