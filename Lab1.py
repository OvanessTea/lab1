import matplotlib.pyplot as pyplot
import control.matlab as matlab
import numpy
import math
import colorama as color

def choice():
    inertialessUnitName = 'Безынерционное звено'
    aperiodUnitName = 'Апериодическое звено'

    needNewChoice = True

    while needNewChoice:
        print(color.Style.RESET_ALL)
        userInput = input('Введите номер команды: \n'
                          '1 - ' + inertialessUnitName + ';\n'
                          '2 - ' + aperiodUnitName + '.\n')
        if userInput.isdigit():
            needNewChoice = False
            userInput = int(userInput)
            if userInput == 1:
                name = 'Безынерционное звено'
            elif userInput == 2:
                name = 'Апериодическое звено'
            else:
                print(color.Fore.RED + '\nНедоступное значение')
                needNewChoice = True

        else:
            print(color.Fore.RED + '\nПожалуйста, введите числовое значение.\n')
            needNewChoice = True
    return name

def getUnit(name):
    needNewChoice = True
    while needNewChoice:
        needNewChoice = False
        k = input('Пожалуйста, введите коэффициент "k": ')
        T = input('Пожалуйста, введите коэффициент "T": ')

        if k.isdigit() and T.isdigit():
            k = int(k)
            T = int(T)
            if name == 'Безынерционное звено':
                unit = matlab.tf([k], [1])
            elif name == 'Апериодическое звено':
                unit = matlab.tf([k], [T, 1])
        else:
            print(color.Fore.RED + '\nПожалуйста, введите числовое значение.\n')
            needNewChoice = True
    return unit

def graph(num, title, y, x):
    pyplot.subplot(2, 1, num)
    pyplot.grid(True)
    if title == 'Переходная характеристика':
        pyplot.plot(x, y, 'purple')
    elif title == 'Импульсная характеристика':
        pyplot.plot(x, y, 'green')
    pyplot.title(title)
    pyplot.ylabel('Амплитуда')
    pyplot.xlabel('Время (c)')

unitName = choice()
unit = getUnit(unitName)

timeLine = []
for i in range(0, 1):
    timeLine.append(i)
[y, x] = matlab.step(unit, timeLine)
graph(1, 'Переходная характеристика', y, x)
[y, x] = matlab.impulse(unit, timeLine)
graph(2, 'Импульсная характеристика', y, x)

