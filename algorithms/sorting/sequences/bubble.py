"""
Алгоритм: сортировка последовательности пузырьком.
Временная сложность (средняя): O(n^2).
Временная сложность (лучшая): O(n).
Пространственная сложность: O(1).

Описание: последовательность сортируется на месте путём повторного
прохода по списку с обменом соседних элементов, расположенных
в неправильном порядке.
"""

from typing import TypeVar

T = TypeVar("T", bound=int | float)


def sort_bubble(input_sequence: list[T]) -> None:
    """Сортирует последовательность на месте методом пузырьковой сортировки.

    Алгоритм последовательно проходит по списку, сравнивая соседние элементы
    и меняя их местами, если они расположены в неправильном порядке.
    Процесс повторяется до тех пор, пока за проход не было выполнено ни одной
    перестановки, что указывает на завершение сортировки.

    Аргументы:
        input_sequence: список целых или вещественных чисел для сортировки.
            Список изменяется на месте.

    Возвращает:
        None. Результат сортировки сохраняется во входном списке.

    Примеры:
        >>> numbers = [5, 2, 8, 1, 3]
        >>> sort_bubble(numbers)
        >>> numbers
        [1, 2, 3, 5, 8]
    """
    for outer_index in range(len(input_sequence)):
        is_swapped = False
        for inner_index in range(len(input_sequence) - outer_index - 1):
            if input_sequence[inner_index] > input_sequence[inner_index + 1]:
                is_swapped = True
                (
                    input_sequence[inner_index],
                    input_sequence[inner_index + 1],
                ) = (
                    input_sequence[inner_index + 1],
                    input_sequence[inner_index],
                )

        if not is_swapped:
            break
