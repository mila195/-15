
import sys
from logic import evaluate_rpn, validate_expression

def print_header():
    print("\n" + "=" * 70)
    print("          КАЛЬКУЛЯТОР ОБРАТНОЙ ПОЛЬСКОЙ ЗАПИСИ")
    print("=" * 70)
    print("  Программа вычисляет арифметические выражения в постфиксной форме")
    print("  Поддерживаемые операции: +, -, *, /")
    print("  Операнды: вещественные положительные числа")
    print("=" * 70)


def print_menu():
    print("\n  ГЛАВНОЕ МЕНЮ:")
    print("  ┌────────────────────────────────────────────────────────────┐")
    print("  │  1. Ввести выражение вручную                             │")
    print("  │  2. Вычислить выражение из файла                        │")
    print("  │  3. Показать информацию и примеры                       │")
    print("  │  4. Выход из программы                                  │")
    print("  └────────────────────────────────────────────────────────────┘")


def print_examples():
    print("\n  ПРИМЕРЫ ВЫРАЖЕНИЙ:")
    print("  ┌────────────────────────────────────────────────────────────┐")
    print("  │  Инфиксная форма          Постфиксная форма              │")
    print("  ├────────────────────────────────────────────────────────────┤")
    print("  │  a - b                    a b -                          │")
    print("  │  a * b + c                a b * c +                      │")
    print("  │  a * (b + c)              a b c + *                      │")
    print("  │  a + b / c / d * e        a b c / d / e * +              │")
    print("  └────────────────────────────────────────────────────────────┘")

    print("\n  ПРИМЕРЫ ВЫЧИСЛЕНИЙ:")
    print("  ┌─────────────────────┬────────────────────────────────────┐")
    print("  │  Выражение           │  Результат                       │")
    print("  ├─────────────────────┼────────────────────────────────────┤")
    print("  │  3 4 +              │  7  (3 + 4)                      │")
    print("  │  10 2 /             │  5  (10 / 2)                     │")
    print("  │  3 4 + 2 *          │  14 ((3 + 4) * 2)               │")
    print("  │  5 2 / 3 +          │  5.5 (5 / 2 + 3)                │")
    print("  │  2 3 4 * + 5 /      │  2.8 ((2 + 3 * 4) / 5)          │")
    print("  └─────────────────────┴────────────────────────────────────┘")


def get_user_expression():
    print("\n  Введите выражение в обратной польской записи:")
    print("    - Числа и операторы разделяйте пробелами")
    print("    - Используйте только операторы: +, -, *, /")
    print("    - Пример: 3 4 + 2 *")

    while True:
        expression = input("  > ").strip()
        if expression:
            return expression
        print("  ! Ошибка: выражение не может быть пустым")
        print("  Попробуйте снова.")


def calculate_manually():
    """
    Режим ручного ввода выражения.
    """
    print("\n" + "=" * 70)
    print("          ВВОД ВЫРАЖЕНИЯ ВРУЧНУЮ")
    print("=" * 70)

    # Получение выражения от пользователя
    expression = get_user_expression()

    # Валидация выражения
    is_valid, error_message = validate_expression(expression)
    if not is_valid:
        print(f"\n  ! Ошибка валидации: {error_message}")
        print("  Проверьте правильность ввода.")
        return

    # Вычисление выражения
    try:
        result = evaluate_rpn(expression)

        # Вывод результата
        print("\n" + "-" * 70)
        print("  РЕЗУЛЬТАТ ВЫЧИСЛЕНИЯ:")
        print(f"    Выражение: {expression}")
        print(f"    Результат: {result}")
        print("-" * 70)

    except ValueError as error:
        print(f"\n  ! Ошибка в выражении: {error}")
    except ZeroDivisionError as error:
        print(f"\n  ! {error}")
    except Exception as error:
        print(f"\n  ! Непредвиденная ошибка: {error}")
        print("  Пожалуйста, сообщите разработчику.")


def calculate_from_file():
    """
    Режим чтения выражения из файла.
    """
    print("\n" + "=" * 70)
    print("          ВЫЧИСЛЕНИЕ ИЗ ФАЙЛА")
    print("=" * 70)

    # Запрос имени файла
    filename = input("  Введите имя файла: ").strip()

    if not filename:
        print("  ! Ошибка: имя файла не может быть пустым")
        return

    # Чтение файла
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            expression = file.read().strip()

        # Проверка, что файл не пуст
        if not expression:
            print("  ! Ошибка: файл пуст")
            return

        print(f"\n  Содержимое файла: {expression}")

        # Валидация выражения
        is_valid, error_message = validate_expression(expression)
        if not is_valid:
            print(f"\n  ! Ошибка в файле: {error_message}")
            return

        # Вычисление выражения
        result = evaluate_rpn(expression)

        # Вывод результата
        print("\n" + "-" * 70)
        print("  РЕЗУЛЬТАТ ВЫЧИСЛЕНИЯ:")
        print(f"    Файл: {filename}")
        print(f"    Выражение: {expression}")
        print(f"    Результат: {result}")
        print("-" * 70)

    except FileNotFoundError:
        print(f"\n  ! Ошибка: файл '{filename}' не найден")
        print("  Проверьте правильность имени файла.")
    except PermissionError:
        print(f"\n  ! Ошибка: нет прав для чтения файла '{filename}'")
    except ValueError as error:
        print(f"\n  ! Ошибка в выражении: {error}")
    except ZeroDivisionError as error:
        print(f"\n  ! {error}")
    except Exception as error:
        print(f"\n  ! Непредвиденная ошибка: {error}")
        print("  Пожалуйста, сообщите разработчику.")


def show_information():
    """
    Выводит информацию о программе.
    """
    print("\n" + "=" * 70)
    print("          ИНФОРМАЦИЯ О ПРОГРАММЕ")
    print("=" * 70)

    print("\n  НАЗНАЧЕНИЕ:")
    print("    Вычисление арифметических выражений, записанных")
    print("    в обратной польской записи (постфиксной форме).")

    print("\n  АЛГОРИТМ РАБОТЫ:")
    print("    1. Входное выражение разбивается на токены (числа и операторы)")
    print("    2. Для каждого токена:")
    print("       - Если токен - число, он помещается в стек")
    print("       - Если токен - оператор, из стека извлекаются")
    print("         два последних числа, выполняется операция,")
    print("         результат помещается в стек")
    print("    3. После обработки всех токенов на вершине стека")
    print("       находится результат вычисления")

    print("\n  ИСПОЛЬЗУЕМАЯ СТРУКТУРА ДАННЫХ:")
    print("    Стек (LIFO - Last In, First Out)")
    print("    Реализован с помощью собственного класса Stack")

    print("\n  ПОДДЕРЖИВАЕМЫЕ ОПЕРАЦИИ:")
    print("    +  сложение")
    print("    -  вычитание")
    print("    *  умножение")
    print("    /  деление (с проверкой деления на ноль)")

    print("\n  ТИПЫ ДАННЫХ:")
    print("    Вещественные числа (положительные)")
    print("    Результат возвращается в виде int или float")

    print("\n  ФОРМАТ ВВОДА:")
    print("    Числа и операторы разделяются одним пробелом")
    print("    Пример: 3 4 + 2 *")

    print_examples()
    print("\n" + "=" * 70)


def main():
    while True:
        # Вывод заголовка и меню
        print_header()
        print_menu()

        # Получение выбора пользователя
        choice = input("\n  Выберите пункт меню (1-4): ").strip()

        # Обработка выбора
        if choice == '1':
            calculate_manually()
            input("\n  Нажмите Enter для продолжения...")

        elif choice == '2':
            calculate_from_file()
            input("\n  Нажмите Enter для продолжения...")

        elif choice == '3':
            show_information()
            input("\n  Нажмите Enter для продолжения...")

        elif choice == '4':
            print("\n" + "=" * 70)
            print("  Спасибо за использование программы!")
            print("  До свидания!")
            print("=" * 70)
            sys.exit(0)

        else:
            print("\n  ! Ошибка: некорректный выбор")
            print("  Пожалуйста, выберите число от 1 до 4.")
            input("\n  Нажмите Enter для продолжения...")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n  Программа прервана пользователем.")
        sys.exit(0)
    except Exception as error:
        print(f"\n  Критическая ошибка: {error}")
        print("  Программа будет завершена.")
        sys.exit(1)