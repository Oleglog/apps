def calculate(num1,  num2, action):
    if action == "+":
        return num1 + num2
    elif action == "-":
        return num1 - num2
    elif action == "*":
        return num1 * num2
    elif action == "/":
        if num2 == 0:
            raise ValueError('Ошибка, деление на ноль невозможно')
        else:
            return num1 / num2
    else:
        raise ValueError('Неверная операция')
    
def main():
    print('Калкьулятор')
    print('доступные действия: (+, -, *, /)')

    num1 = float(input('Введите первое число: '))
    action = input('Выберите дейсвтие: (+, -, *, /)')
    num2 = float(input('Введите второе число: '))

    result = calculate(num1, num2, action)
    print (f"Результат: {num1} {action} {num2} = {result}")


if __name__ == "__main__":
    main()

    