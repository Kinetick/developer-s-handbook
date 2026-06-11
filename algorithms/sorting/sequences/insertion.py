"""
Алгоритм: сортировка последовательности вставками.
Временная сложность (средняя): O(n^2).
Временная сложность (лучшая): O(n).
Пространственная сложность: O(1).

Описание: алгоритм последовательно берет элементы из неотсортированной
части и вставляет их на правильные позиции в уже отсортированной части.
"""

from typing import TypeVar

T = TypeVar("T", bound=int | float)


def sort_insertion(input_sequence: list[T]) -> None:
    """Сортирует последовательность на месте методом сортировки вставками.

    Алгоритм рассматривает список как состоящий из двух частей: отсортированной
    (изначально содержит только первый элемент) и неотсортированной.
    На каждом шаге берется следующий элемент из неотсортированной части и
    вставляется в нужную позицию в отсортированной части путем сдвига
    более крупных элементов вправо.

    Аргументы:
        input_sequence: список целых или вещественных чисел для сортировки.
            Список изменяется на месте.

    Возвращает:
        None. Результат сортировки сохраняется во входном списке.

    Примеры:
        >>> numbers = [12, 11, 13, 5, 6]
        >>> sort_insertion(numbers)
        >>> numbers
        [5, 6, 11, 12, 13]
    """
    for current_index in range(1, len(input_sequence)):
        key = input_sequence[current_index]
        previous_index = current_index - 1

        while previous_index >= 0 and input_sequence[previous_index] > key:
            input_sequence[previous_index + 1] = input_sequence[previous_index]
            previous_index -= 1

        input_sequence[previous_index + 1] = key
