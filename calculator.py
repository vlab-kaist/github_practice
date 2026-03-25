class Calculator:
    def __init__(self):
        self.history = []

    def add(self, a, b):
        result = a + b
        self.history.append(f"{a} + {b} = {result}")
        return result

    def subtract(self, a, b):
        result = a - b
        self.history.append(f"{a} - {b} = {result}")
        return result

    def multiply(self, a, b):
        result = a * b
        self.history.append(f"{a} * {b} = {result}")
        return result

    def divide(self, a, b):
        if b == 0:
            raise ZeroDivisionError("0으로 나눌 수 없습니다")
        result = a / b
        self.history.append(f"{a} / {b} = {result}")
        return result

    def power(self, a, b):
        result = a ** b
        self.history.append(f"{a} ^ {b} = {result}")
        return result

    def modulo(self, a, b):
        if b == 0:
            raise ZeroDivisionError("0으로 나눌 수 없습니다")
        result = a % b
        self.history.append(f"{a} % {b} = {result}")
        return result

    def get_history(self):
        return self.history

    def clear_history(self):
        self.history = []


if __name__ == "__main__":
    calc = Calculator()
    print(calc.add(10, 5))
    print(calc.subtract(10, 5))
    print(calc.multiply(10, 5))
    print(calc.divide(10, 5))
    print(calc.power(2, 10))
    print(calc.modulo(17, 3))
    print("기록:", calc.get_history())
