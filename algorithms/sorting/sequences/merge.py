"""
Алгоритм: сортировка последовательности слиянием.
Временная сложность: O(n log n).
Пространственная сложность: O(n).

Описание: алгоритм рекурсивно делит последовательность пополам,
сортирует каждую половину, а затем сливает две отсортированные
части в одну.
"""

from collections import deque
from typing import TypeVar

T = TypeVar("T", bound=int | float)


def sort_merge_dequeue(input_sequence: list[T]) -> list[T]:
    """Сортирует последовательность методом слияния с использованием deque.

    Рекурсивно делит список пополам, сортирует каждую часть, затем
    сливает две отсортированные очереди, сравнивая их первые элементы.

    Аргументы:
        input_sequence: список целых или вещественных чисел для сортировки.

    Возвращает:
        Новый отсортированный список. Исходный список не изменяется.

    Примеры:
        >>> numbers = [38, 27, 43, 3, 9, 82, 10]
        >>> sorted_numbers = sort_merge_dequeue(numbers)
        >>> sorted_numbers
        [3, 9, 10, 27, 38, 43, 82]
    """
    if len(input_sequence) < 2:
        return input_sequence
    elif len(input_sequence) == 2 and input_sequence[0] > input_sequence[1]:
        input_sequence[0], input_sequence[1] = (
            input_sequence[1],
            input_sequence[0],
        )
        return input_sequence

    pivot_index = len(input_sequence) // 2
    left_part = deque(sort_merge_dequeue(input_sequence[:pivot_index]))
    right_part = deque(sort_merge_dequeue(input_sequence[pivot_index:]))

    result = []
    while left_part and right_part:
        if left_part[0] < right_part[0]:
            result.append(left_part.popleft())
        elif left_part[0] > right_part[0]:
            result.append(right_part.popleft())
        else:
            result.append(left_part.popleft())
            result.append(right_part.popleft())

    result.extend(left_part)
    result.extend(right_part)

    return result


def sort_merge_iter(input_sequence: list[T]) -> list[T]:
    """Сортирует последовательность методом слияния с использованием
    итераторов.

    Рекурсивно делит список пополам, сортирует каждую часть, затем
    сливает две отсортированные последовательности, используя итераторы
    для поэлементного доступа.

    Аргументы:
        input_sequence: список целых или вещественных чисел для сортировки.

    Возвращает:
        Новый отсортированный список. Исходный список не изменяется.

    Примеры:
        >>> numbers = [38, 27, 43, 3, 9, 82, 10]
        >>> sorted_numbers = sort_merge_iter(numbers)
        >>> sorted_numbers
        [3, 9, 10, 27, 38, 43, 82]
    """
    if len(input_sequence) < 2:
        return input_sequence
    elif len(input_sequence) == 2 and input_sequence[0] > input_sequence[1]:
        input_sequence[0], input_sequence[1] = (
            input_sequence[1],
            input_sequence[0],
        )
        return input_sequence

    pivot_index = len(input_sequence) // 2

    left_part = iter(sort_merge_dequeue(input_sequence[:pivot_index]))
    right_part = iter(sort_merge_dequeue(input_sequence[pivot_index:]))
    left_item = next(left_part, None)
    right_item = next(right_part, None)

    result = []
    while left_item is not None and right_item is not None:
        if left_item <= right_item:
            result.append(left_item)
            left_item = next(left_part, None)
        else:
            result.append(right_item)
            right_item = next(right_part, None)

    if left_item is not None:
        result.append(left_item)
    if right_item is not None:
        result.append(right_item)

    result.extend(left_part)
    result.extend(right_part)

    return result
