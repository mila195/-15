
class Stack:
    """
    Класс, реализующий структуру данных "Стек" (LIFO).
    """

    def __init__(self):
        """Инициализация пустого стека."""
        self._items = []

    def push(self, item):
        self._items.append(item)

    def pop(self):
        if self.is_empty():
            raise IndexError("Стек пуст")
        return self._items.pop()

    def peek(self):
        if self.is_empty():
            raise IndexError("Стек пуст")
        return self._items[-1]

    def is_empty(self):
        """
        Проверяет, пуст ли стек.

        Возвращает:
            bool: True если стек пуст, иначе False
        """
        return len(self._items) == 0

    def size(self):
        """
        Возвращает количество элементов в стеке.

        Возвращает:
            int: размер стека
        """
        return len(self._items)

    def clear(self):
        """Очищает стек."""
        self._items.clear()


def is_operator(token):
    return token in ('+', '-', '*', '/')

def is_number(token):
    try:
        float(token)
        return True
    except ValueError:
        return False


def apply_operator(operator, operand1, operand2):
    """
    Применяет арифметическую операцию к двум операндам.
    """
    if operator == '+':
        return operand1 + operand2
    elif operator == '-':
        return operand1 - operand2
    elif operator == '*':
        return operand1 * operand2
    elif operator == '/':
        if operand2 == 0:
            raise ZeroDivisionError("Деление на ноль")
        return operand1 / operand2
    else:
        raise ValueError(f"Неизвестный оператор: {operator}")


def evaluate_rpn(expression):
    """
    Вычисляет значение выражения в обратной польской записи.
    """
    # Проверка на пустое выражение
    if not expression or not expression.strip():
        raise ValueError("Выражение не может быть пустым")

    # Разбиваем строку на токены
    tokens = expression.strip().split()

    # Создаем стек для операндов
    stack = Stack()

    # Обрабатываем каждый токен
    for token in tokens:
        if is_number(token):
            # Число → в стек
            stack.push(float(token))
        elif is_operator(token):
            # Оператор → извлекаем два операнда
            if stack.size() < 2:
                raise ValueError(
                    f"Недостаточно операндов для операции '{token}'"
                )
            operand2 = stack.pop()  # правый операнд
            operand1 = stack.pop()  # левый операнд

            # Выполняем операцию
            result = apply_operator(token, operand1, operand2)

            # Результат → в стек
            stack.push(result)
        else:
            raise ValueError(f"Некорректный токен: '{token}'")

    # Проверка: в стеке должен быть ровно один элемент
    if stack.size() != 1:
        raise ValueError(
            f"В стеке осталось {stack.size()} элементов, должно быть 1"
        )

    # Получаем результат
    result = stack.pop()

    # Форматируем результат
    if result.is_integer():
        return int(result)
    else:
        return round(result, 10)


def validate_expression(expression):
    # Проверка на пустое выражение
    if not expression or not expression.strip():
        return False, "Выражение не может быть пустым"

    tokens = expression.strip().split()

    # Проверка минимальной длины
    if len(tokens) < 3:
        return False, "Выражение должно содержать минимум 3 элемента"

    # Проверка каждого токена
    for token in tokens:
        if not is_number(token) and not is_operator(token):
            return False, f"Некорректный токен: '{token}'"

    # Подсчет операндов и операторов
    operand_count = sum(1 for token in tokens if is_number(token))
    operator_count = sum(1 for token in tokens if is_operator(token))

    # Проверка наличия операторов
    if operator_count == 0:
        return False, "Выражение не содержит операторов"

    # Проверка соотношения операндов и операторов
    if operand_count != operator_count + 1:
        return False, (
            f"Некорректное соотношение: операндов {operand_count}, "
            f"операторов {operator_count}"
        )

    return True, ""


class NumberNode:
    pass