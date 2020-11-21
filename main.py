def get_help():
    print("The program performs addition and subtraction of numbers")

from collections import deque


def infix_to_postfix(infixexpr):
        prec = {}
        prec["*"] = 3
        prec["/"] = 3
        prec["^"] = 3
        prec["+"] = 2
        prec["-"] = 2
        prec["("] = 1
        opStack = deque()
        postfixList = []
        tokenList = infixexpr.split()

        for token in tokenList:
            if token[0] in "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz" or token[0] in "0123456789":
                postfixList.append(token)
            elif token == '(':
                opStack.append(token)
            elif token == ')':
                topToken = opStack.pop()
                while topToken != '(':
                    postfixList.append(topToken)
                    topToken = opStack.pop()
            else:
                while (len(opStack) > 0) and \
                        (prec[opStack[len(opStack) - 1]] >= prec[token]):
                    postfixList.append(opStack.pop())
                opStack.append(token)

        while len(opStack) > 0:
            postfixList.append(opStack.pop())
        return " ".join(postfixList)

def doMath(op, op1, op2):
    if op == "*":
        return op1 * op2
    elif op == "/":
        return op1 / op2
    elif op == "+":
        return op1 + op2
    elif op == "^":
        return pow(op1, op2)
    else:
        return op1 - op2

def postfixEval(postfixExpr, variables):
    operandStack = deque()
    tokenList = postfixExpr.split()

    for token in tokenList:
        if token[0] in "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz" or token[0] in "0123456789":
            operandStack.append(token)
        else:
            operand2 = operandStack.pop()
            if operand2.isalpha():
                if operand2 in variables.keys():
                    operand2 = float(variables[operand2])
                else:
                    return "Unknown variable"
            operand1 = operandStack.pop()
            if operand1.isalpha():
                if operand1 in variables.keys():
                    operand1 = float(variables[operand1])
                else:
                    return "Unknown variable"
            result = str(doMath(token, float(operand1), float(operand2)))
            operandStack.append(result)
    return float(operandStack.pop())


def convert_to_spaces(input_):
    if '(' in input_:
        input_ = input_.replace('(', '( ')
    if ')' in input_:
        input_ = input_.replace(')', ' )')
    if '+' in input_:
        input_ = input_.replace('+', ' + ')
    if '-' in input_:
        input_ = input_.replace('-', ' - ')
    if '*' in input_:
        input_ = input_.replace('*', ' * ')
    if '/' in input_:
        input_ = input_.replace('/', ' / ')
    if '^' in input_:
        input_ = input_.replace('^', ' ^ ')
    return input_

def remove_multisign(input_):
    while '--' in input_:
        input_ = input_.replace('--', '+')
    while '++' in input_:
        input_ = input_.replace('++', '+')
    if '+-' in input_:
        input_ = input_.replace('+-', '-')
    elif '-+' in input_:
        input_ = input_.replace('-+', '-')
    return input_

def check_brackets(input_):
    my_stack = []
    for symbol in input_:
        if symbol == '(':
            my_stack.append(symbol)
        elif symbol == ')':
            if len(my_stack) > 0:
                my_stack.pop()
                continue
            else:
                return "ERROR"
    if len(my_stack) > 0:
        return "ERROR"
    else:
        return "OK"

def command_check(input_):
    if input_ == '/exit':
        return 'exit'
    elif input_ == '/help':
        return 'help'
    else:
        return 'unknown command'

def show_value(input_, variables):
    if (not input_.isdigit()) and (not input_.isalpha()):
        print("Invalid identifier")
    elif input_.isdigit():
        print(input_)
    elif input_.isalpha():
        if input_ in variables.keys():
            print(variables[input_])
        else:
            print("Unknown variable")

def variable_assignment(input_, variables):
    input_parts = input_.replace(" ","")
    input_parts = input_parts.split("=")
    if len(input_parts) != 2:
        print("Invalid assignment")
    elif not input_parts[0].isalpha():
        print("Invalid identifier")
    elif (not input_parts[1].isdigit()) and (not input_parts[1].isalpha()) and (input_parts[1][0] != '-'):
        print("Invalid identifier")
    elif input_parts[1].isalpha() and (input_parts[1] not in variables.keys()):
            print("Unknown variable")
    else:
        if input_parts[1].isalpha():
            variables[input_parts[0]] = variables[input_parts[1]]
        else:
            variables[input_parts[0]] = int(input_parts[1])

def calculate(input_, variables):
    if '(' in input_ or ')' in input_:
        if check_brackets(input_) == 'ERROR':
            return 'Invalid expression'
    if ' ' in input_:
        input_ = input_.replace(' ', '')
    if input_[len(input_)-1] == '+' or input_[len(input_)-1] == '-' or input_[len(input_)-1] == '*' or input_[len(input_)-1] == '/' or input_[len(input_)-1] == '^':
        return 'Invalid expression'
    elif '**' in input_ or '//' in input_ or '^^' in input_:
        return 'Invalid expression'
    elif '++' in input_ or '--' in input_:
        input_ = remove_multisign(input_)
    input_ = convert_to_spaces(input_)
    input_ = infix_to_postfix(input_)
    result = postfixEval(input_, variables)
    number_dec = str(result - int(result))[1:]
    if number_dec[1] == '0':
        result = int(round(result))
    return result


# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    variables = dict()
    while True:
        input_ = input().strip()
        if input_ == '':
            continue
        if input_.isalpha():
            show_value(input_, variables)
            continue
        elif input_[0] == "/":
            if command_check(input_) == "exit":
                print("Bye!")
                break
            elif command_check(input_) == "help":
                get_help()
            else:
                print("Unknown command")
        elif '=' in input_:
            variable_assignment(input_, variables)
        elif input_.isdigit() or input_[1:].isdigit():
            try:
                print(int(input_))
            except Exception:
                print("Invalid expression")
        else:
            try:
                print(calculate(input_,variables))
            except Exception:
                print("Invalid expression")