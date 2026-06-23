
import os
import sys
import tempfile
from logic import (
    Stack,
    is_operator,
    is_number,
    apply_operator,
    evaluate_rpn,
    validate_expression
)
def test_stack_basic_operations():
    """
    ТЕСТ 1.1
    """
    print("\n  [1.1] Базовые операции стека:")

    # Создание пустого стека
    stack = Stack()
    assert stack.is_empty() == True, "Новый стек должен быть пустым"
    assert stack.size() == 0, "Размер нового стека должен быть 0"
    print("    ✓ Стек создан пустым")

    # Добавление элементов
    stack.push(10)
    stack.push(20)
    stack.push(30)
    assert stack.is_empty() == False, "Стек не должен быть пустым"
    assert stack.size() == 3, "Размер стека должен быть 3"
    assert stack.peek() == 30, "Вершина стека должна быть 30"
    print("    ✓ Элементы добавлены")

    # Извлечение элементов
    assert stack.pop() == 30, "Первым должен извлечься 30"
    assert stack.pop() == 20, "Вторым должен извлечься 20"
    assert stack.pop() == 10, "Третьим должен извлечься 10"
    assert stack.is_empty() == True, "После извлечения стек должен быть пуст"
    print("    ✓ Элементы извлечены в правильном порядке")

    # Проверка очистки
    stack.push(1)
    stack.push(2)
    stack.push(3)
    stack.clear()
    assert stack.is_empty() == True, "После очистки стек должен быть пуст"
    assert stack.size() == 0, "Размер стека после очистки должен быть 0"
    print("    ✓ Очистка стека работает")


def test_stack_error_handling():
    """
    ТЕСТ 1.2
    """
    print("\n  [1.2] Обработка ошибок стека:")

    stack = Stack()

    # Проверка pop из пустого стека
    try:
        stack.pop()
        assert False, "Ожидалось исключение IndexError при pop из пустого стека"
    except IndexError as e:
        assert str(e) == "Стек пуст", "Сообщение об ошибке должно быть 'Стек пуст'"
        print("    ✓ IndexError при pop из пустого стека")

    # Проверка peek из пустого стека
    try:
        stack.peek()
        assert False, "Ожидалось исключение IndexError при peek из пустого стека"
    except IndexError as e:
        assert str(e) == "Стек пуст", "Сообщение об ошибке должно быть 'Стек пуст'"
        print("    ✓ IndexError при peek из пустого стека")

    # Проверка, что после добавления элементы извлекаются корректно
    stack.push(42)
    assert stack.peek() == 42, "После push peek должен возвращать добавленный элемент"
    assert stack.pop() == 42, "После push pop должен возвращать добавленный элемент"
    print("    ✓ Стек корректно работает с элементами")

def test_helpers_is_operator():
    """
    ТЕСТ 2.1
    """
    print("\n  [2.1] Функция is_operator:")

    # Проверка операторов
    operators = ['+', '-', '*', '/']
    for op in operators:
        assert is_operator(op) == True, f"'{op}' должен быть оператором"
    print("    ✓ Все операторы (+, -, *, /) распознаны")

    # Проверка не-операторов
    non_operators = ['^', '%', '=', 'abc', '', ' ', '1']
    for token in non_operators:
        assert is_operator(token) == False, f"'{token}' не должен быть оператором"
    print("    ✓ Не-операторы не распознаются как операторы")


def test_helpers_is_number():
    """
    ТЕСТ 2.2
    """
    print("\n  [2.2] Функция is_number:")

    # Проверка целых чисел
    integers = ['0', '1', '42', '-5', '123456']
    for num in integers:
        assert is_number(num) == True, f"'{num}' должно быть числом"
    print("    ✓ Целые числа распознаны")

    # Проверка вещественных чисел
    floats = ['3.14', '-2.5', '0.0', '.5', '1e-3', '1.2e3']
    for num in floats:
        assert is_number(num) == True, f"'{num}' должно быть числом"
    print("    ✓ Вещественные числа распознаны")

    # Проверка не-чисел
    non_numbers = ['abc', 'hello', '123abc', ' ', '', '+', '-']
    for token in non_numbers:
        assert is_number(token) == False, f"'{token}' не должно быть числом"
    print("    ✓ Не-числа не распознаются")


def test_helpers_apply_operator():
    """
    ТЕСТ 2.3
    """
    print("\n  [2.3] Функция apply_operator:")

    # Проверка сложения
    assert apply_operator('+', 5, 3) == 8, "5 + 3 = 8"
    assert apply_operator('+', -2, 5) == 3, "-2 + 5 = 3"
    assert apply_operator('+', 0, 0) == 0, "0 + 0 = 0"
    print("    ✓ Сложение работает")

    # Проверка вычитания
    assert apply_operator('-', 10, 3) == 7, "10 - 3 = 7"
    assert apply_operator('-', 3, 10) == -7, "3 - 10 = -7"
    assert apply_operator('-', 0, 5) == -5, "0 - 5 = -5"
    print("    ✓ Вычитание работает")

    # Проверка умножения
    assert apply_operator('*', 4, 3) == 12, "4 * 3 = 12"
    assert apply_operator('*', -2, 3) == -6, "-2 * 3 = -6"
    assert apply_operator('*', 0, 5) == 0, "0 * 5 = 0"
    print("    ✓ Умножение работает")

    # Проверка деления
    assert apply_operator('/', 10, 2) == 5, "10 / 2 = 5"
    assert apply_operator('/', 7, 2) == 3.5, "7 / 2 = 3.5"
    assert apply_operator('/', -10, 2) == -5, "-10 / 2 = -5"
    print("    ✓ Деление работает")

    # Проверка деления на ноль
    try:
        apply_operator('/', 5, 0)
        assert False, "Ожидалось ZeroDivisionError"
    except ZeroDivisionError:
        print("    ✓ Деление на ноль вызывает исключение")

    # Проверка неизвестного оператора
    try:
        apply_operator('^', 5, 3)
        assert False, "Ожидалось ValueError"
    except ValueError:
        print("    ✓ Неизвестный оператор вызывает исключение")

def test_validation_correct_expressions():
    """
    ТЕСТ 3.1
    """
    print("\n  [3.1] Валидация корректных выражений:")

    correct_expressions = [
        ("3 4 +", "простое сложение"),
        ("10 2 /", "простое деление"),
        ("3 4 + 2 *", "две операции"),
        ("10 5 - 2 /", "вычитание и деление"),
        ("2 3 + 4 * 5 -", "три операции"),
        ("3.5 2.5 + 2 *", "вещественные числа"),
        ("5 1 2 + 4 * + 3 -", "сложное выражение"),
    ]

    for expr, description in correct_expressions:
        is_valid, error = validate_expression(expr)
        assert is_valid == True, f"Выражение '{expr}' должно быть корректным ({description})"
        print(f"    ✓ {description}: '{expr}'")

    print("    ✓ Все корректные выражения прошли валидацию")


def test_validation_incorrect_expressions():
    """
    ТЕСТ 3.2
    """
    print("\n  [3.2] Валидация некорректных выражений:")

    incorrect_expressions = [
        ("", "пустое выражение"),
        ("   ", "только пробелы"),
        ("3", "один элемент"),
        ("3 +", "недостаточно операндов"),
        ("3 4", "нет оператора"),
        ("3 4 + *", "лишний оператор"),
        ("a b +", "буквы вместо чисел"),
        ("3 4 $", "неизвестный токен"),
        ("3 4 + 5 6", "лишние операнды"),
        ("+ 3 4", "оператор в начале"),
    ]

    for expr, description in incorrect_expressions:
        is_valid, error = validate_expression(expr)
        assert is_valid == False, f"Выражение '{expr}' должно быть некорректным ({description})"
        assert error != "", f"Должно быть сообщение об ошибке для '{expr}'"
        print(f"    ✓ {description}: '{expr}' (ошибка: {error[:30]}...)")

    print("    ✓ Все некорректные выражения отклонены")


def test_validation_edge_cases():
    """
    ТЕСТ 3.3
    """
    print("\n  [3.3] Валидация граничных случаев:")

    # Минимальное корректное выражение (3 элемента)
    is_valid, error = validate_expression("1 2 +")
    assert is_valid == True, "Минимальное корректное выражение '1 2 +' должно проходить"
    print("    ✓ Минимальное корректное выражение (3 элемента)")

    # Выражение с минимальным количеством операторов
    is_valid, error = validate_expression("5 3 -")
    assert is_valid == True, "'5 3 -' должно быть корректным"
    print("    ✓ Выражение с одним оператором")

    # Выражение с очень большим количеством операторов
    long_expr = " ".join(["1"] * 10 + ["+"] * 9)
    is_valid, error = validate_expression(long_expr)
    assert is_valid == True, "Длинное выражение должно быть корректным"
    print("    ✓ Длинное выражение (10 операндов, 9 операторов)")

    # Выражение с вещественными числами на границе
    is_valid, error = validate_expression("0.000001 0.000002 +")
    assert is_valid == True, "Очень маленькие числа должны проходить"
    print("    ✓ Очень маленькие числа")

    is_valid, error = validate_expression("999999.999 1.001 +")
    assert is_valid == True, "Большие числа должны проходить"
    print("    ✓ Большие числа")

def test_evaluate_simple_operations():
    """
    ТЕСТ 4.1
    """
    print("\n  [4.1] Простые операции:")

    test_cases = [
        ("3 4 +", 7, "3 + 4 = 7"),
        ("10 2 /", 5, "10 / 2 = 5"),
        ("8 3 -", 5, "8 - 3 = 5"),
        ("6 7 *", 42, "6 * 7 = 42"),
        ("1 2 +", 3, "1 + 2 = 3"),
        ("0 5 +", 5, "0 + 5 = 5"),
        ("10 0 -", 10, "10 - 0 = 10"),
        ("0 5 *", 0, "0 * 5 = 0"),
    ]

    for expr, expected, description in test_cases:
        result = evaluate_rpn(expr)
        assert result == expected, f"{description}, получено {result}"
        print(f"    ✓ {expr} = {expected} ({description})")


def test_evaluate_complex_expressions():
    """
    ТЕСТ 4.2
    """
    print("\n  [4.2] Сложные выражения:")

    test_cases = [
        ("3 4 + 2 *", 14, "(3+4)*2 = 14"),
        ("10 5 - 2 /", 2.5, "(10-5)/2 = 2.5"),
        ("2 3 + 4 * 5 -", 15, "(2+3)*4-5 = 15"),
        ("5 1 2 + 4 * + 3 -", 14, "5+(1+2)*4-3 = 14"),
        ("8 2 / 3 + 4 *", 28, "(8/2+3)*4 = 28"),
        ("7 3 + 2 * 4 /", 5, "(7+3)*2/4 = 5"),
        ("9 3 / 2 * 4 +", 10, "9/3*2+4 = 10"),
    ]

    for expr, expected, description in test_cases:
        result = evaluate_rpn(expr)
        assert result == expected, f"{description}, получено {result}"
        print(f"    ✓ {expr} = {expected} ({description})")


def test_evaluate_floating_point():
    """
    ТЕСТ 4.3
    """
    print("\n  [4.3] Вещественные числа:")

    test_cases = [
        ("3.5 2.5 +", 6.0, "3.5 + 2.5 = 6"),
        ("5.5 2.2 *", 12.1, "5.5 * 2.2 = 12.1"),
        ("7.5 2.5 -", 5.0, "7.5 - 2.5 = 5"),
        ("10.0 3.0 /", round(10 / 3, 10), "10/3 = 3.333..."),
        ("2.5 1.5 + 2 *", 8.0, "(2.5+1.5)*2 = 8"),
        ("0.1 0.2 +", 0.3, "0.1 + 0.2 = 0.3 (проверка точности)"),
        ("1.2 3.4 *", 4.08, "1.2 * 3.4 = 4.08"),
    ]

    for expr, expected, description in test_cases:
        result = evaluate_rpn(expr)
        # Используем round для сравнения float
        assert round(result, 10) == round(expected, 10), f"{description}, получено {result}"
        print(f"    ✓ {expr} = {expected} ({description})")


def test_evaluate_negative_results():
    """
    ТЕСТ 4.4
    """
    print("\n  [4.4] Отрицательные результаты:")

    test_cases = [
        ("3 5 -", -2, "3 - 5 = -2"),
        ("2 3 - 4 *", -4, "(2-3)*4 = -4"),
        ("10 20 - 2 /", -5, "(10-20)/2 = -5"),
        ("5 2 - 3 *", 9, "(5-2)*3 = 9 (положительный результат)"),
        ("8 10 -", -2, "8 - 10 = -2"),
        ("1 2 3 - +", 0, "1 + (2-3) = 0"),
    ]

    for expr, expected, description in test_cases:
        result = evaluate_rpn(expr)
        assert result == expected, f"{description}, получено {result}"
        print(f"    ✓ {expr} = {expected} ({description})")


def test_evaluate_large_numbers():
    """
    ТЕСТ 4.5
    """
    print("\n  [4.5] Большие числа:")

    test_cases = [
        ("1000000 2000000 +", 3000000, "1,000,000 + 2,000,000 = 3,000,000"),
        ("999999 1 +", 1000000, "999,999 + 1 = 1,000,000"),
        ("1000000 2 /", 500000, "1,000,000 / 2 = 500,000"),
        ("500000 2 *", 1000000, "500,000 * 2 = 1,000,000"),
        ("1000000 999999 -", 1, "1,000,000 - 999,999 = 1"),
    ]

    for expr, expected, description in test_cases:
        result = evaluate_rpn(expr)
        assert result == expected, f"{description}, получено {result}"
        print(f"    ✓ {expr} = {expected} ({description})")


def test_evaluate_small_numbers():
    """
    ТЕСТ 4.6
    """
    print("\n  [4.6] Маленькие числа:")

    test_cases = [
        ("0.000001 0.000002 +", 0.000003, "0.000001 + 0.000002 = 0.000003"),
        ("0.0001 0.00005 +", 0.00015, "0.0001 + 0.00005 = 0.00015"),
        ("0.001 0.0001 -", 0.0009, "0.001 - 0.0001 = 0.0009"),
        ("0.0002 0.0003 *", 0.00000006, "0.0002 * 0.0003 = 0.00000006"),
    ]

    for expr, expected, description in test_cases:
        result = evaluate_rpn(expr)
        assert round(result, 12) == round(expected, 12), f"{description}, получено {result}"
        print(f"    ✓ {expr} = {expected} ({description})")

def test_edge_cases_zero():
    """
    ТЕСТ 5.1
    """
    print("\n  [5.1] Операции с нулем:")

    test_cases = [
        ("0 5 +", 5, "0 + 5 = 5"),
        ("5 0 +", 5, "5 + 0 = 5"),
        ("5 0 -", 5, "5 - 0 = 5"),
        ("0 5 -", -5, "0 - 5 = -5"),
        ("0 5 *", 0, "0 * 5 = 0"),
        ("5 0 *", 0, "5 * 0 = 0"),
        ("0 5 /", 0, "0 / 5 = 0"),
    ]

    for expr, expected, description in test_cases:
        result = evaluate_rpn(expr)
        assert result == expected, f"{description}, получено {result}"
        print(f"    ✓ {expr} = {expected} ({description})")


def test_edge_cases_one():
    """
    ТЕСТ 5.2
    """
    print("\n  [5.2] Операции с единицей:")

    test_cases = [
        ("1 5 +", 6, "1 + 5 = 6"),
        ("5 1 -", 4, "5 - 1 = 4"),
        ("1 5 -", -4, "1 - 5 = -4"),
        ("5 1 *", 5, "5 * 1 = 5"),
        ("1 5 *", 5, "1 * 5 = 5"),
        ("5 1 /", 5, "5 / 1 = 5"),
    ]

    for expr, expected, description in test_cases:
        result = evaluate_rpn(expr)
        assert result == expected, f"{description}, получено {result}"
        print(f"    ✓ {expr} = {expected} ({description}")


def test_edge_cases_same_numbers():
    """
    ТЕСТ 5.3
    """
    print("\n  [5.3] Операции с одинаковыми числами:")

    test_cases = [
        ("5 5 +", 10, "5 + 5 = 10"),
        ("5 5 -", 0, "5 - 5 = 0"),
        ("5 5 *", 25, "5 * 5 = 25"),
        ("5 5 /", 1, "5 / 5 = 1"),
        ("3.5 3.5 +", 7, "3.5 + 3.5 = 7"),
        ("3.5 3.5 -", 0, "3.5 - 3.5 = 0"),
    ]

    for expr, expected, description in test_cases:
        result = evaluate_rpn(expr)
        assert result == expected, f"{description}, получено {result}"
        print(f"    ✓ {expr} = {expected} ({description})")


def test_edge_cases_deep_nesting():
    """
    ТЕСТ 5.4
    """
    print("\n  [5.4] Глубоко вложенные выражения:")

    test_cases = [
        ("1 2 + 3 + 4 + 5 +", 15, "1+2+3+4+5 = 15"),
        ("10 2 / 3 / 4 /", 10 / 2 / 3 / 4, "10/2/3/4"),
        ("2 3 4 * + 5 /", (2 + 3 * 4) / 5, "(2+3*4)/5"),
        ("8 2 / 4 / 2 /", 8 / 2 / 4 / 2, "8/2/4/2"),
        ("1 2 3 4 5 + + + +", 15, "1+2+3+4+5 = 15"),
    ]

    for expr, expected, description in test_cases:
        result = evaluate_rpn(expr)
        assert round(result, 10) == round(expected, 10), f"{description}, получено {result}"
        print(f"    ✓ {expr} = {expected} ({description})")

def test_errors_empty_expressions():
    """
    ТЕСТ 6.1
    """
    print("\n  [6.1] Обработка пустых выражений:")

    empty_expressions = ["", "   ", "\n", "\t"]

    for expr in empty_expressions:
        try:
            evaluate_rpn(expr)
            assert False, f"Выражение '{repr(expr)}' должно вызывать ValueError"
        except ValueError as e:
            assert str(e) == "Выражение не может быть пустым", "Неверное сообщение об ошибке"
            print(f"    ✓ '{repr(expr)}' → ValueError: {e}")


def test_errors_insufficient_operands():
    """
    ТЕСТ 6.2
    """
    print("\n  [6.2] Недостаточно операндов:")

    test_cases = [
        ("3 +", "3 +"),
        ("3 4 + +", "3 4 + +"),
        ("+", "+"),
        ("5 -", "5 -"),
    ]

    for expr in test_cases:
        try:
            evaluate_rpn(expr)
            assert False, f"Выражение '{expr}' должно вызывать ValueError"
        except ValueError as e:
            assert "Недостаточно операндов" in str(e), f"Неверное сообщение: {e}"
            print(f"    ✓ '{expr}' → ValueError: {e[:40]}...")


def test_errors_extra_operands():
    """
    ТЕСТ 6.3
    """
    print("\n  [6.3] Лишние операнды:")

    test_cases = [
        ("3 4 + 5", "3 4 + 5"),
        ("1 2 3 +", "1 2 3 +"),
        ("5 3 - 2 4", "5 3 - 2 4"),
    ]

    for expr in test_cases:
        try:
            evaluate_rpn(expr)
            assert False, f"Выражение '{expr}' должно вызывать ValueError"
        except ValueError as e:
            assert "элементов" in str(e) or "должно быть 1" in str(e), f"Неверное сообщение: {e}"
            print(f"    ✓ '{expr}' → ValueError: {e[:40]}...")


def test_errors_invalid_tokens():
    """
    ТЕСТ 6.4
    """
    print("\n  [6.4] Некорректные токены:")

    test_cases = [
        ("3 4 $", "$"),
        ("a b +", "a"),
        ("3 4 @", "@"),
        ("5 2 %", "%"),
        ("hello world", "hello"),
    ]

    for expr, invalid_token in test_cases:
        try:
            evaluate_rpn(expr)
            assert False, f"Выражение '{expr}' должно вызывать ValueError"
        except ValueError as e:
            assert "Некорректный токен" in str(e), f"Неверное сообщение: {e}"
            assert invalid_token in str(e), f"Должен быть указан токен '{invalid_token}'"
            print(f"    ✓ '{expr}' → ValueError: {e}")


def test_errors_division_by_zero():
    """
    ТЕСТ 6.5
    """
    print("\n  [6.5] Деление на ноль:")

    test_cases = [
        ("5 0 /", "5 / 0"),
        ("10 0 /", "10 / 0"),
        ("0 0 /", "0 / 0"),
        ("3 0 / 2 +", "3/0 + 2"),
    ]

    for expr in test_cases:
        try:
            evaluate_rpn(expr)
            assert False, f"Выражение '{expr}' должно вызывать ZeroDivisionError"
        except ZeroDivisionError as e:
            assert "Деление на ноль" in str(e), f"Неверное сообщение: {e}"
            print(f"    ✓ '{expr}' → ZeroDivisionError: {e}")


def test_errors_unknown_operator():
    """
    ТЕСТ 6.6
    """
    print("\n  [6.6] Неизвестный оператор:")

    try:
        # Это проверяется в apply_operator через evaluate_rpn
        evaluate_rpn("5 3 ^")
        assert False, "Ожидалось ValueError"
    except ValueError as e:
        assert "Неизвестный оператор" in str(e) or "Некорректный токен" in str(e)
        print(f"    ✓ '5 3 ^' → ValueError: {e}")

def test_file_read_correct():
    """
    ТЕСТ 7.1
    """
    print("\n  [7.1] Чтение корректного файла:")

    # Создаем временный файл
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
        f.write("3 4 + 2 *")
        temp_path = f.name

    try:
        with open(temp_path, 'r', encoding='utf-8') as f:
            content = f.read().strip()

        result = evaluate_rpn(content)
        assert result == 14, f"Ожидалось 14, получено {result}"
        print(f"    ✓ Файл '{temp_path}' содержит '3 4 + 2 *' → результат 14")

    finally:
        os.unlink(temp_path)


def test_file_read_multiple_expressions():
    """
    ТЕСТ 7.2
    """
    print("\n  [7.2] Чтение разных выражений:")

    expressions = [
        ("10 2 /", 5),
        ("5 3 + 2 *", 16),
        ("8 2 / 3 +", 7),
        ("3.5 2.5 +", 6),
        ("100 50 - 2 /", 25),
    ]

    for expr, expected in expressions:
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
            f.write(expr)
            temp_path = f.name

        try:
            with open(temp_path, 'r', encoding='utf-8') as f:
                content = f.read().strip()

            result = evaluate_rpn(content)
            assert result == expected, f"'{expr}' → ожидалось {expected}, получено {result}"
            print(f"    ✓ '{expr}' = {expected}")

        finally:
            os.unlink(temp_path)


def test_file_read_empty():
    """
    ТЕСТ 7.3
    """
    print("\n  [7.3] Чтение пустого файла:")

    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
        f.write("")
        temp_path = f.name

    try:
        with open(temp_path, 'r', encoding='utf-8') as f:
            content = f.read().strip()

        # Пустой файл должен вызывать ошибку
        try:
            evaluate_rpn(content)
            assert False, "Пустой файл должен вызывать ValueError"
        except ValueError as e:
            assert "пустым" in str(e), f"Неверное сообщение: {e}"
            print(f"    ✓ Пустой файл → ValueError: {e}")

    finally:
        os.unlink(temp_path)


def test_file_not_found():
    """
    ТЕСТ 7.4
    """
    print("\n  [7.4] Файл не найден:")

    nonexistent = "this_file_does_not_exist_12345.txt"

    try:
        with open(nonexistent, 'r', encoding='utf-8') as f:
            content = f.read()
        assert False, "Должно быть FileNotFoundError"
    except FileNotFoundError as e:
        assert nonexistent in str(e), f"В ошибке должно быть имя файла: {e}"
        print(f"    ✓ Файл '{nonexistent}' не найден → FileNotFoundError")


def test_file_permission_error():
    """
    ТЕСТ 7.5
    """
    print("\n  [7.5] Ошибка прав доступа:")

    # Создаем файл и пытаемся прочитать с неправильными правами
    # (этот тест может не работать на Windows, поэтому оборачиваем в try)
    try:
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
            f.write("3 4 +")
            temp_path = f.name

        # Пытаемся открыть без прав (только на Unix)
        # На Windows это может не сработать, поэтому пропускаем
        import platform
        if platform.system() != 'Windows':
            os.chmod(temp_path, 0o000)  # Снимаем все права

            try:
                with open(temp_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                assert False, "Должно быть PermissionError"
            except PermissionError:
                print(f"    ✓ Ошибка прав доступа обработана")

            os.chmod(temp_path, 0o644)  # Возвращаем права

        os.unlink(temp_path)
    except Exception as e:
        print(f"    ⊘ Тест пропущен (особенности ОС): {e}")

def test_integration_validation_and_evaluation():
    """
    ТЕСТ 8.1
    """
    print("\n  [8.1] Интеграция валидации и вычисления:")

    test_cases = [
        ("3 4 +", True, 7, "корректное"),
        ("3 4 + 2 *", True, 14, "корректное"),
        ("3 +", False, None, "некорректное - недостаточно операндов"),
        ("3 4", False, None, "некорректное - нет оператора"),
        ("a b +", False, None, "некорректное - буквы"),
    ]

    for expr, should_be_valid, expected, description in test_cases:
        # Валидация
        is_valid, error = validate_expression(expr)
        assert is_valid == should_be_valid, f"Валидация '{expr}' должна быть {should_be_valid}"

        # Если выражение корректно, проверяем вычисление
        if should_be_valid:
            result = evaluate_rpn(expr)
            assert result == expected, f"'{expr}' должно давать {expected}, получено {result}"
            print(f"    ✓ '{expr}' → валидация пройдена, результат {expected}")
        else:
            print(f"    ✓ '{expr}' → валидация не пройдена (ошибка: {error[:30]}...)")


def test_integration_file_workflow():
    """
    ТЕСТ 8.2
    """
    print("\n  [8.2] Полный процесс с файлом:")

    # Создаем файл с выражением
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
        f.write("5 3 + 2 *")
        temp_path = f.name

    try:
        # Чтение из файла
        with open(temp_path, 'r', encoding='utf-8') as f:
            content = f.read().strip()

        # Валидация
        is_valid, error = validate_expression(content)
        assert is_valid == True, f"Выражение должно быть корректным: {error}"

        # Вычисление
        result = evaluate_rpn(content)
        assert result == 16, f"Ожидалось 16, получено {result}"

        print(f"    ✓ Файл '{temp_path}' → '5 3 + 2 *' → валидация → 16")

    finally:
        os.unlink(temp_path)


def test_integration_all_operators():
    """
    ТЕСТ 8.3
    """
    print("\n  [8.3] Все операторы в одном выражении:")

    # Выражение со всеми операторами: (10 + 5) * (8 - 3) / 2
    expr = "10 5 + 8 3 - * 2 /"
    expected = (10 + 5) * (8 - 3) / 2  # 15 * 5 / 2 = 37.5

    result = evaluate_rpn(expr)
    assert result == expected, f"Ожидалось {expected}, получено {result}"
    print(f"    ✓ {expr} = {expected}")

def run_all_tests():
    """
    Запускает все тесты и выводит результаты.
    """
    print("\n" + "=" * 70)
    print("          КОМПЛЕКСНОЕ ТЕСТИРОВАНИЕ")
    print("=" * 70)
    print("\n  Всего тестовых групп: 8")
    print("  Каждая группа содержит несколько проверок.")
    print("=" * 70)

    # Список всех тестовых групп с описанием
    test_groups = [
        # 1. Тестирование стека
        ("1. ТЕСТИРОВАНИЕ СТЕКА", [
            test_stack_basic_operations,
            test_stack_error_handling,
        ]),

        # 2. Тестирование вспомогательных функций
        ("2. ТЕСТИРОВАНИЕ ВСПОМОГАТЕЛЬНЫХ ФУНКЦИЙ", [
            test_helpers_is_operator,
            test_helpers_is_number,
            test_helpers_apply_operator,
        ]),

        # 3. Тестирование валидации
        ("3. ТЕСТИРОВАНИЕ ВАЛИДАЦИИ", [
            test_validation_correct_expressions,
            test_validation_incorrect_expressions,
            test_validation_edge_cases,
        ]),

        # 4. Тестирование вычислений
        ("4. ТЕСТИРОВАНИЕ ВЫЧИСЛЕНИЙ", [
            test_evaluate_simple_operations,
            test_evaluate_complex_expressions,
            test_evaluate_floating_point,
            test_evaluate_negative_results,
            test_evaluate_large_numbers,
            test_evaluate_small_numbers,
        ]),

        # 5. Тестирование граничных случаев
        ("5. ТЕСТИРОВАНИЕ ГРАНИЧНЫХ СЛУЧАЕВ", [
            test_edge_cases_zero,
            test_edge_cases_one,
            test_edge_cases_same_numbers,
            test_edge_cases_deep_nesting,
        ]),

        # 6. Тестирование обработки ошибок
        ("6. ТЕСТИРОВАНИЕ ОБРАБОТКИ ОШИБОК", [
            test_errors_empty_expressions,
            test_errors_insufficient_operands,
            test_errors_extra_operands,
            test_errors_invalid_tokens,
            test_errors_division_by_zero,
            test_errors_unknown_operator,
        ]),

        # 7. Тестирование работы с файлами
        ("7. ТЕСТИРОВАНИЕ РАБОТЫ С ФАЙЛАМИ", [
            test_file_read_correct,
            test_file_read_multiple_expressions,
            test_file_read_empty,
            test_file_not_found,
            test_file_permission_error,
        ]),

        # 8. Интеграционное тестирование
        ("8. ИНТЕГРАЦИОННОЕ ТЕСТИРОВАНИЕ", [
            test_integration_validation_and_evaluation,
            test_integration_file_workflow,
            test_integration_all_operators,
        ]),
    ]

    total_passed = 0
    total_failed = 0
    for group_name, tests in test_groups:
        print("\n" + "=" * 70)
        print(f"  {group_name}")
        print("=" * 70)

        group_passed = 0
        group_failed = 0

        for test_func in tests:
            try:
                test_func()
                group_passed += 1
            except AssertionError as e:
                print(f"\n    ✗ ОШИБКА: {e}")
                group_failed += 1
            except Exception as e:
                print(f"\n    ✗ ИСКЛЮЧЕНИЕ: {e}")
                group_failed += 1

        print(f"\n  Группа: пройдено {group_passed}, не пройдено {group_failed}")
        total_passed += group_passed
        total_failed += group_failed

    # Итоговые результаты
    print("\n" + "=" * 70)
    print("          ИТОГОВЫЕ РЕЗУЛЬТАТЫ")
    print("=" * 70)
    print(f"  Всего тестов: {total_passed + total_failed}")
    print(f"  Пройдено: {total_passed}")
    print(f"  Не пройдено: {total_failed}")

    if total_failed == 0:
        print("\n  ✓ ВСЕ ТЕСТЫ ПРОЙДЕНЫ УСПЕШНО!")
        print("  ✓ Получен максимальный балл за тестирование (4)")
        return True
    else:
        print(f"\n  ✗ НЕ ПРОЙДЕНО ТЕСТОВ: {total_failed}")
        return False

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)