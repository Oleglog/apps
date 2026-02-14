import unittest
from main import calculate

class TestCalculator(unittest.TestCase):

    #верные тесты
    def test_plus(self):
        self.assertEqual(calculate(5, 3, "+"), 8)
        self.assertEqual(calculate(-1, 1, "+"), 0)
    
    def test_minus(self):
        self.assertEqual(calculate(4, 1, "-"), 3)
        self.assertEqual(calculate(10, 8, "-"), 2)

    def test_multiplication(self):
        self.assertEqual(calculate(4, 4, "*"), 16)
        self.assertEqual(calculate(2, 10, "*"), 20)

    def test_devision(self):
        self.assertEqual(calculate(5, 1, "/"), 5)
        self.assertEqual(calculate(20, 5, "/"), 4)


    #Неверные тесты
    def test_plus_bad(self):
        self.assertEqual(calculate(5, 3, "+"), 2)
        self.assertEqual(calculate(-1, 1, "+"), 1)
    
    def test_minus_bad(self):
        self.assertEqual(calculate(4, 1, "-"), 2)
        self.assertEqual(calculate(10, 8, "-"), 1)

    def test_multiplication_bad(self):
        self.assertEqual(calculate(4, 4, "*"), 25)
        self.assertEqual(calculate(2, 10, "*"), 244)

    def test_devision_bad(self):
        self.assertEqual(calculate(5, 1, "/"), 23)
        self.assertEqual(calculate(20, 5, "/"), 56)
    

    #Деление на ноль
    def test_division_by_zero(self):
        with self.assertRaises(ValueError) as context:
            calculate(10, 0, "/")
        self.assertEqual(str(context.exception), 'Ошибка, деление на ноль невозможно')

    #Неверная операция
    def test_invalid_action(self):
        with self.assertRaises(ValueError) as context:
            calculate(10, 0, "%")
        self.assertEqual(str(context.exception), 'Неверная операция')
    

if __name__ == "__main__":
    unittest.main()