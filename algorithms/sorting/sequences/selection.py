"""
Алгоритм: сортировка последовательности выбором.
Временная сложность: O(n^2).
Пространственная сложность: O(1).

Описание: на каждом шаге алгоритм находит минимальный элемент в
неотсортированной части последовательности и меняет его местами с
первым элементом этой части.
"""

from typing import TypeVar

T = TypeVar("T", bound=int | float)


def sort_selection(input_sequence: list[T]) -> None:
    """Сортирует последовательность на месте методом сортировки выбором.

    На каждом шаге алгоритм находит минимальный элемент в неотсортированной
    части списка и меняет его местами с первым элементом этой части.
    Граница между отсортированной и неотсортированной частями постепенно
    смещается вправо.

    Аргументы:
        input_sequence: список целых или вещественных чисел для сортировки.
            Список изменяется на месте.

    Возвращает:
        None. Результат сортировки сохраняется во входном списке.

    Примеры:
        >>> numbers = [64, 25, 12, 22, 11]
        >>> sort_selecting(numbers)
        >>> numbers
        [11, 12, 22, 25, 64]
    """
    for outer_index in range(len(input_sequence)):
        min_value_index = outer_index
        for inner_index in range(outer_index, len(input_sequence)):
            if input_sequence[min_value_index] > input_sequence[inner_index]:
                min_value_index = inner_index

        if min_value_index != outer_index:
            input_sequence[min_value_index], input_sequence[outer_index] = (
                input_sequence[outer_index],
                input_sequence[min_value_index],
            )
