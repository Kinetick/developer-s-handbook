"""
Алгоритм: быстрая сортировка последовательности.
Временная сложность (средняя): O(n log n).
Временная сложность (худшая): O(n^2).
Пространственная сложность (оригинал): O(n log n).
Пространственная сложность (Ломуто): O(log n).

Описание: алгоритм выбирает опорный элемент и разделяет последовательность
на три части: элементы меньше опорного, равные ему и большие. Затем
рекурсивно сортирует части «меньше» и «больше».
"""

from typing import TypeVar

T = TypeVar("T", bound=int | float)


def sort_quick_orig(input_sequence: list[T], is_uniq: bool = True) -> list[T]:
    """Сортирует последовательность методом быстрой сортировки (оригинал).

    Создаёт новые списки для элементов меньше, равных и больше опорного.
    Рекурсивно сортирует части и объединяет результат.

    Аргументы:
        input_sequence: список целых или вещественных чисел для сортировки.
        is_uniq: если True, то элементы, равные опорному, считаются
            уникальными (только один экземпляр). Если False, все равные
            элементы собираются в отдельную группу.

    Возвращает:
        Новый отсортированный список. Исходный список не изменяется.

    Примеры:
        >>> numbers = [3, 6, 8, 10, 1, 2, 1]
        >>> sorted_numbers = sort_quick_orig(numbers)
        >>> sorted_numbers
        [1, 1, 2, 3, 6, 8, 10]
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
    pivot_item = input_sequence[pivot_index]
    lt_part = [x for x in input_sequence if x < pivot_item]
    gt_part = [x for x in input_sequence if x > pivot_item]
    eq_part = [pivot_item]
    if not is_uniq:
        eq_part = [x for x in input_sequence if x == pivot_item]

    result = (
        sort_quick_orig(lt_part, is_uniq)
        + eq_part
        + sort_quick_orig(gt_part, is_uniq)
    )

    return result


def sort_quick_lomuto(
    input_sequence: list[T], start_index: int, end_index: int
) -> None:
    """Сортирует последовательность на месте методом быстрой сортировки Ломуто.

    Использует схему разбиения Ломуто, где опорный элемент выбирается
    как последний в текущем диапазоне. Элементы меньше или равные опорному
    перемещаются влево, а большие — остаются справа.

    Аргументы:
        input_sequence: список целых или вещественных чисел для сортировки.
            Список изменяется на месте.
        start_index: начальный индекс сортируемого диапазона (включительно).
        end_index: конечный индекс сортируемого диапазона (включительно).

    Примеры:
        >>> numbers = [10, 7, 8, 9, 1, 5]
        >>> sort_quick_lomuto(numbers, 0, len(numbers) - 1)
        >>> numbers
        [1, 5, 7, 8, 9, 10]
    """
    if start_index < end_index:
        pivot_index = end_index
        sorted_border = start_index - 1
        for sentinel_index in range(start_index, end_index):
            if input_sequence[sentinel_index] <= input_sequence[pivot_index]:
                sorted_border += 1
                (
                    input_sequence[sorted_border],
                    input_sequence[sentinel_index],
                ) = (
                    input_sequence[sentinel_index],
                    input_sequence[sorted_border],
                )
        input_sequence[sorted_border + 1], input_sequence[pivot_index] = (
            input_sequence[pivot_index],
            input_sequence[sorted_border + 1],
        )
        sorted_border += 1

        sort_quick_lomuto(input_sequence, start_index, sorted_border - 1)
        sort_quick_lomuto(input_sequence, sorted_border + 1, end_index)
