import re


def validate_fitness(fitness: str):
    OPERATING = r'(PV|PI|TV|TI|SW|SP|SO|V|T|\-?\d*\.?\d+)'
    OPERATOR = r'(\+|\-|\*|/|\*\*)'
    PATTERN = f'^{OPERATING}({OPERATOR}{OPERATING})*$'

    equation_without_parentheses = fitness.replace('(', '').replace(')', '')

    parentheses = 0
    for caracter in fitness:
        if caracter == ' ':
            continue

        if caracter == '(':
            parentheses += 1
            continue

        if caracter == ')':
            parentheses -= 1
            continue
    if parentheses != 0:
        print('parenteses')
        return False

    if re.match(PATTERN, equation_without_parentheses) is None:
        print('pattern')
        return False
    else:
        return True


if __name__ == '__main__':
    text = [
        'TV - TI',
        '(PV * 2 + TV * 3 + SO * 10 + V * 100) / T',
        '(PV + TV + SO) * 10 - (PI + TI) * 5',
        '((PV + TV) * 2 + SO * 20 + V * 200) / (T + 1)',
        '(PV ** 2 + TV ** 2) / (PI + TI + 1)',
        '((PV + TV) ** 2 + SO * 50 + V * 500) / (T + 1)',
        '(PV + TV) - (PI + TI)',
        '(PV * 2 + TV * 3) - (PI * 2 + TI)',
        '(SO * 50 + V * 100) - (PI * 10 + TI * 5)',
        '(PV + TV + SO * 10) / T',
        '(PV * 5 + TV * 10 + SO * 100 + V * 500) / T',
        '(PV + TV) * (SO + SW)',
        '(PV * 2 + TV * 3) / T',
        '(PV + PI + TV + TI) / T',
        '(PV * TV) + (PI * TI)',
        '(PV + TV) * (PV + TV)',
        '(PV + PI) ** 2',
        '(TV + TI) ** 3',
        'PV ** 2 + TV ** 2',
        'T / 2',
        '(SO + SW) ** 2 / T',
        '(PV + TV) ** 2 + (PI + TI) ** 2',
        'PV + PI * 2',
        'TV * 3 + TI',
        '(PV + PI) / T',
        '(SO + SW) * 5 * 0.2',
        'V * 10 / T',
        'PV * TV + PI * TI',
        '(PV + TV) / (PI + TI)',
        '((PV * -1)+(PI*-100)+(TI*-100)+(TV*100)+(SW*-100)+(SP*-100)+(SO*100)+(V*1000))/ T',
    ]

    for f in text:
        print(validate_fitness(f.replace(' ', '')), f)
