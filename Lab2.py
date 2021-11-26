import matplotlib.pyplot as pyplot
import control.matlab as matlab
import numpy
import sympy
from numpy import linalg as LA
from sympy.solvers import solve
from sympy import Symbol

koc = 2

def stabilityTest(koc):

    # Исходные данные
    #################################################
    ky = 21
    tg = 8
    ty = 5
    # Турбина - паро
    tpt = 5
    kpt = 1
    # Обратная связь - гибкая
    #################################################

    # Передаточная функция  обратной связи:
    woc = matlab.tf([koc, 0], [0, 1])

    # Передаточная функция генератора:
    wg = matlab.tf([1], [tg, 1])

    # Передаточная функция паровой турбины:
    wt = matlab.tf([kpt], [tpt, 1])

    # Передаточная функция исполнительного устройства:
    wy = matlab.tf([ky], [ty, 1])

    # Эквивалентная передаточная функция
    equivalentLink = matlab.feedback(wy * wg * wt, woc, -1)
    print(equivalentLink)

    # Построение переходной характеристики
    [y, x] = matlab.step(equivalentLink)
    pyplot.plot(x, y)
    pyplot.title('Переходная характеристика')
    pyplot.ylabel('Амплитуда')
    pyplot.xlabel('Время, сек')
    pyplot.grid(True)
    pyplot.show()

    # -----------------------------------------Проверка устойчивости САУ--------------------------------------------------

    sauPoles = matlab.pole(equivalentLink)
    sauZeros = matlab.zero(equivalentLink)
    print('Полюса передаточной функции:\n', sauPoles)
    print('Нули передаточной функции:\n', sauZeros)

    systemStability = True

    # Проверка устойчивости системы
    for i in sauPoles:
        if i.real > 0:
            systemStability = False
            break

    # Вывод сообщения о устойчивости / неустойчивости системы
    print('Система устойчива' if systemStability else 'Система неустойчива')

    # -----------------------------------------Проверка по критерию Найквиста---------------------------------------------

    # Размыкание САУ и оценка устойчивости по критерию Найквиста
    openSau = wt * wg * wy
    print(openSau)

    # Вывод диаграммы Найквиста
    matlab.nyquist(openSau)
    pyplot.grid(True)
    pyplot.title('Nyquist Diagram of openSau(s) = 21/(200 * s^3 + 105 * s^2 + 18 * s + 1)')
    pyplot.xlabel('Re(s)')
    pyplot.ylabel('Im(s)')
    pyplot.show()

    # -----------------------------------------Определение запаса устойчивости---------------------------------------------

    # Снятие логарифмической амплитудно-частотной и логарифмической фазов-частотной характеристик разомкнутой системы
    matlab.bode(openSau, dB=False)
    pyplot.plot()
    axes = pyplot.gcf().get_axes()
    axes[0].set_title("ЛАЧХ")
    axes[1].set_title("ЛФЧХ")
    pyplot.xlabel('Частота, Гц')
    pyplot.show()

    # -----------------------------------------Проверка по критерию Михайлова---------------------------------------------

    # Суммирование числителя и знаменателя эквивалентной передаточной функции
    numeratorOfSAU = [float(x) for x in equivalentLink.num[0][0]]
    denominatorOfSAY = [float(x) for x in equivalentLink.den[0][0]]
    functionMikhailov = []
    for i in range(len(denominatorOfSAY) - len(numeratorOfSAU)):
        numeratorOfSAU.insert(0, 0)
    for i in range(len(numeratorOfSAU)):
        functionMikhailov.append(numeratorOfSAU[i] + denominatorOfSAY[i])
    functionGurvitz = functionMikhailov
    print(functionMikhailov)
    # Проверка устойчивости
    functionMikhailov = functionMikhailov[::-1]
    j = sympy.I
    omega = sympy.symbols("w")
    for i in range(len(functionMikhailov)):
        functionMikhailov[i] = functionMikhailov[i] * (j * omega) ** i
    x = numpy.arange(0, 1, 0.01)
    mc = []
    for i in x:
        summ = 0
        for k in functionMikhailov:
            summ += k.subs(omega, i)
        mc.append(summ)

    real = [sympy.re(x) for x in mc]
    imaginary = [sympy.im(x) for x in mc]
    numberOfAxisCrossings = 1
    flagCrossing = False
    flagPossibleCrossingX = True
    flagPossibleCrossingY = True
    for i in range(len(mc) - 1):
        if ((real[i] >= 0 and real[i + 1] <= 0) or (real[i] <= 0 and real[i + 1] >= 0)):
            if flagPossibleCrossingX:
                numberOfAxisCrossings += 1
                flagPossibleCrossingX = False
                flagPossibleCrossingY = True
            if imaginary[i] > 0:
                flagCrossing = True
        if ((imaginary[i] >= 0 and imaginary[i + 1] <= 0) or (imaginary[i] <= 0 and imaginary[i + 1] >= 0)):
            if flagPossibleCrossingY:
                numberOfAxisCrossings += 1
                flagPossibleCrossingX = True
                flagPossibleCrossingY = False
    if numberOfAxisCrossings >= 3 and flagCrossing:
        print('Система устойчива по критерию Михайлова')
    else:
        print('Система устойчива по критерию Михайлова')

    # Построение годографа Михайлова
    pyplot.title('Годограф Михайлова')
    ax = pyplot.gca()
    ax.plot(real, imaginary)
    ax.grid(True)
    ax.spines['left'].set_position('zero')
    ax.spines['right'].set_color('none')
    ax.spines['bottom'].set_position('zero')
    ax.spines['top'].set_color('none')
    pyplot.xlim(-25, 50)
    pyplot.ylim(-25, 15)
    pyplot.xlabel("re")
    pyplot.ylabel("im")
    pyplot.show()

    # -----------------------------------------Проверка по критерию Гурвица-----------------------------------------------

    # Построение матрицы и расчет ее определителя
    print(functionGurvitz)
    oddNumbersOfMatrix=[]
    evenNumbersOfMatrix=[]
    for i in range(0, len(functionGurvitz), 2):
        evenNumbersOfMatrix.append(functionGurvitz[i])
    for i in range(1, len(functionGurvitz)+1, 2):
        oddNumbersOfMatrix.append(functionGurvitz[i])
    matrix = [oddNumbersOfMatrix, evenNumbersOfMatrix]
    print('matrix', matrix)
    determinantOfMatrix = LA.det(matrix)
    print("determinantOfMatrix", determinantOfMatrix)

    # Проверка устойчивости по критерию Гурвица?
    if determinantOfMatrix < 0 or matrix[0][0] < 0 or matrix[1][0] < 0:
        print('Система неустойчива по критерию Гурвица')
    else:
        print('Система устойчива по критерию Гурвица')

    x = Symbol('x')
    koc = solve((105*18-200*(1+21*x)), x)

    # Возвращение предельного значения koc
    return koc

newKoc = stabilityTest(koc)
#
# stabilityTest(newKoc)